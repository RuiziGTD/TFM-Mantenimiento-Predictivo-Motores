import os
import tempfile
from tensorflow.keras.models import load_model
from config import CARPETA_OUTPUT_CSV, CARPETA_OUTPUT_DATA_TEST
import numpy as np
from modelo_ia.predict_api import predict_rul

from processing.cleaning import identificar_sensores_irrelevantes_y_guardar
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from api.logs.logging_config import get_logger

logger = get_logger("predict_controller")

router = APIRouter(prefix="/predict", tags=["Predict"])

@router.post("", response_class=JSONResponse)
async def predict(file: UploadFile = File(...)):

    logger.info(f"Predicción solicitada: filename='{file.filename}'")

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

        print("Realizando predicción...")

        y_pred = predict_rul(df)
        logger.info(f"Predicción exitosa: prediccion='{y_pred.tolist()}'")
        return {"prediction": y_pred.tolist()}

    except Exception as e:
        logger.error(f"Error en predicción: filename='{file.filename}', error={e}")
        raise HTTPException(status_code=500, detail=str(e))
