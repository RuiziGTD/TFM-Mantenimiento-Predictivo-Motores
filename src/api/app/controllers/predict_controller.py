from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/predict", tags=["Predict"])

@router.post("", response_class=JSONResponse)
async def predict(file: UploadFile = File(...)):
    try:
        # Leer el contenido del archivo
        contents = await file.read()

        # Aquí iría tu lógica de predicción
        # Por ejemplo, pasar contents a tu modelo de ML

        # Esto es un ejemplo dummy
        result = {"prediction": "motor OK", "filename": file.filename}

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
