from src.ingest.batch_ingest import load_batch
from src.utils.logger import get_logger
from src.processing.cleaning import *
from config import *

logger = get_logger(__name__)

def run_pipeline():
    """
    Ejecuta el pipeline completo sobre una lista de archivos .txt CMAPSS.
    Procesa, filtra sensores irrelevantes y guarda los resultados en CSV.
    """
    try:
        resultados = procesar_varios_archivos_txt(DATA_PATHS_TRAIN)
        logger.info("Pipeline ejecutado correctamente sobre todos los archivos.")
    except Exception as e:
        logger.error(f"Error en el pipeline: {e}")
        print("Error en el pipeline. Revisar logs/pipeline.log para más detalles.")
        return

    print("\nPipeline completado correctamente.")
    return resultados

