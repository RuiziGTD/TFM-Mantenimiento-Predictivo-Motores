import os
import tempfile
from tensorflow.keras.models import load_model
from config import CARPETA_OUTPUT_CSV, CARPETA_OUTPUT_DATA_TEST
import numpy as np

from processing.cleaning import identificar_sensores_irrelevantes_y_guardar
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/predict", tags=["Predict"])

@router.post("", response_class=JSONResponse)
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        params = [None, None]
        
        # Crear archivos temporales con los datos subidos

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        df = identificar_sensores_irrelevantes_y_guardar(
            params,
            path_txt=tmp_path,
            CARPETA_OUTPUT_CSV=CARPETA_OUTPUT_CSV,
            CARPETA_OUTPUT_DATA_TEST=CARPETA_OUTPUT_DATA_TEST
        )

        print("Cargando Modelo LSTM...")

        model = load_model("modelo_ia/lstm_rul.keras")

        print("Modelo cargado, realizando predicción...")

        feature_cols = [
            "op_setting_1", "op_setting_2", "op_setting_3", "T24", "T30", "T50",
            "P30", "Nf", "Nc", "Ps30", "phi", "NRf", "NRc", "BPR", "htBleed", "W31", "W32"
        ]
        sequence_length = 50  # Igual que en entrenamiento

        # Agrupar por motor y construir secuencias
        test_units = df["unit_number"].unique()
        test_units.sort()
        X_test_seq = []
        for unit in test_units:
            unit_data = df[df["unit_number"] == unit][feature_cols].values
            if len(unit_data) < sequence_length:
                pad = np.zeros((sequence_length - len(unit_data), unit_data.shape[1]))
                unit_data = np.vstack([pad, unit_data])
            X_test_seq.append(unit_data[-sequence_length:])
        X_test_seq = np.array(X_test_seq)
        pred = model.predict(X_test_seq, batch_size=64).flatten()
        print("Predicción realizada.")
        print(X_test_seq.shape)  # debe ser (num_motores, sequence_length, num_features)
        print(np.min(X_test_seq), np.max(X_test_seq))  # verifica que esté escalado
        os.remove(tmp_path)

        return {"prediction": pred.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
