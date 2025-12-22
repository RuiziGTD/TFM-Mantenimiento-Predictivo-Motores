from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import io
import os
from pathlib import Path
from api.logs.logging_config import get_logger
from api.app.services.dashboard_service import DashboardService
logger = get_logger("predict_controller")

router = APIRouter(prefix="/predict", tags=["Predict"])

# --- CONFIGURACIÓN ---
CURRENT_DIR = Path(__file__).resolve().parent
SRC_DIR = CURRENT_DIR.parents[2] # CUIDADO CON LAS RUTAS
MODEL_PATH = SRC_DIR.parent / "models" / "lstm_rul.keras"
SCALER_PATH = SRC_DIR.parent / "models" / "minmax_scaler.save"
SEQUENCE_LENGTH = 50 
# Columnas esperadas en el dataset C-MAPSS
FEATURE_COLS = [
    "unit_number", "time_in_cycles", "op_setting_1", "op_setting_2", "op_setting_3",
    "T2", "T24", "T30", "T50", "P2", "P15", "P30", "Nf", "Nc", "epr", "Ps30", "phi",
    "NRf", "NRc", "BPR", "farB", "htBleed", "Nf_dmd", "PCNfR_dmd", "W31", "W32"
]

@router.post("", response_class=JSONResponse)
async def predict(file: UploadFile = File(...)):

    logger.info(f"Predicción solicitada: filename='{file.filename}'")

    try:
        # 1. VALIDACIÓN DE RUTAS
        if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
            raise HTTPException(status_code=500, detail="Modelos no encontrados en el servidor.")
            
        try:
            scaler = joblib.load(SCALER_PATH)
            model = load_model(MODEL_PATH)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error cargando artefactos ML: {str(e)}")

        # 2. LECTURA Y PARSEO DEL ARCHIVO (Soporte Dual: CSV y TXT)
        contents = await file.read()
        
        try:
            # Intento A: CSV con formato estándar (comas)
            df = pd.read_csv(io.BytesIO(contents), sep=",")
            
            # Validación: Si tiene muy pocas columnas, probablemente falló el separador (es un TXT)
            if df.shape[1] < 2: 
                raise ValueError("Formato detectado incorrecto, probando fallback a TXT.")
                
            # Si es un CSV sin cabeceras (solo números), se las asignamos
            if 'op_setting_1' not in df.columns and df.shape[1] >= len(FEATURE_COLS):
                 df = pd.read_csv(io.BytesIO(contents), sep=",", header=None, names=FEATURE_COLS)

        except:
            # Intento B: Formato RAW NASA (espacios y sin cabecera)
            df = pd.read_csv(io.BytesIO(contents), sep=r"\s+", header=None)
            # Recortamos columnas extra generadas por espacios finales y asignamos nombres
            df = df.iloc[:, :len(FEATURE_COLS)]
            df.columns = FEATURE_COLS

        # 3. PREPROCESAMIENTO
        # Eliminar columna objetivo si existe (en archivos de training)
        if 'RUL' in df.columns: 
            df = df.drop(columns=['RUL'])
        
        # Eliminar columnas irrelevantes para este modelo específico
        cols_to_drop = [
            'unit_number', 'time_in_cycles', 
            'T2', 'P2', 'P15', 'epr', 'farB', 'Nf_dmd', 'PCNfR_dmd'
        ]
        # Solo borramos las que existan en el DF actual
        existing_drop = [c for c in cols_to_drop if c in df.columns]
        
        # Guardamos la referencia de los motores para agrupar las secuencias
        units = df['unit_number'].values if 'unit_number' in df.columns else np.zeros(len(df))
        
        df_clean = df.drop(columns=existing_drop)

        # 4. ESCALADO
        try:
            X_scaled = scaler.transform(df_clean)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=f"Error en datos de entrada (Mismatch columnas): {str(ve)}")

        # 5. GENERACIÓN DE SECUENCIAS (SLIDING WINDOW)
        # El modelo fue entrenado con ventanas de 50 ciclos. Ajustamos la predicción en consecuencia.
        X_final = []
        
        unique_units = np.unique(units)
        
        for u in unique_units:
            # Filtrar datos de este motor específico
            idx = np.where(units == u)[0]
            data_unit = X_scaled[idx]
            L = len(data_unit)
            
            # Generar una ventana para cada punto temporal disponible
            for i in range(L):
                # Inicializar ventana con ceros (Padding)
                window = np.zeros((SEQUENCE_LENGTH, data_unit.shape[1]))
                
                end_row = i + 1
                start_row = max(0, end_row - SEQUENCE_LENGTH)
                
                actual_data = data_unit[start_row:end_row]
                
                # Rellenar desde el final hacia atrás
                window[-len(actual_data):] = actual_data
                X_final.append(window)

        X_final = np.array(X_final) 

        # 6. PREDICCIÓN
        predictions = model.predict(X_final)
        logger.info(f"Predicción exitosa: prediccion='{predictions.tolist()}'")
        #return {"prediction": predictions.flatten().tolist()}
        dashboard_view = DashboardService.build_health_view(units, predictions)

        return {
            "prediction": predictions.flatten().tolist(),
            "dashboard": dashboard_view
        }

    except Exception as e:

        logger.error(f"Error en predicción: filename='{file.filename}', error={e}")

        logger.info(f"MODEL_PATH = {MODEL_PATH}")
        logger.info(f"MODEL exists = {MODEL_PATH.exists()}")
        logger.info(f"SCALER_PATH = {SCALER_PATH}")
        logger.info(f"SCALER exists = {SCALER_PATH.exists()}")

        print(f"Error en /predict: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")