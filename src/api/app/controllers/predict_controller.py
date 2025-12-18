import os
import tempfile
from tensorflow.keras.models import load_model
from config import CARPETA_OUTPUT_CSV, CARPETA_OUTPUT_DATA_TEST
import numpy as np
from modelo_ia.modelo_2 import predict_rul

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

        print("Realizando predicción...")

        y_pred = predict_rul(df)

        return {"prediction": y_pred.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
