from src.ingest.batch_ingest import load_batch
from src.utils.logger import get_logger
from src.processing.cleaning import *
from dotenv import load_dotenv
from config import *
import os

load_dotenv(dotenv_path="environment/.env")

DATA_PATH_TRAIN_FD001 = os.getenv("DATA_PATH_TRAIN_FD001")
logger = get_logger(__name__)

def run_pipeline():
    """
    Ejecuta el pipeline completo sobre una lista de archivos .txt CMAPSS.
    Procesa, filtra sensores irrelevantes y guarda los resultados en CSV.
    """

    """
    if not os.path.isdir(CARPETA_OUTPUT):
        print("❌ El directorio no existe.")
        return
    
    archivos = os.listdir(CARPETA_OUTPUT)
    
    # Si hay archivos, no ejecuta la función pipeline.
    if archivos:
        print("⚠️ El directorio tiene archivos, no se ejecuta la función Pipeline.")
        return None
    """
    
    try:
        resultados = procesar_varios_archivos_txt(DATA_PATHS_TEST)
        logger.info("Pipeline ejecutado correctamente sobre todos los archivos.")
    except Exception as e:
        logger.error(f"Error en el pipeline: {e}")
        print("Error en el pipeline. Revisar logs/pipeline.log para más detalles.")
        return

    print("\nPipeline completado correctamente.")
    return resultados

