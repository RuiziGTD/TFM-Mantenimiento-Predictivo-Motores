from src.utils.logger import get_logger
from src.ingest.batch_ingest import *
from dotenv import load_dotenv
from src.config import *
from src.processing.cleaning import *
import os

load_dotenv(dotenv_path="environment/.env")

DATA_PATH_TRAIN_FD001 = os.getenv("DATA_PATH_TRAIN_FD001")
logger = get_logger(__name__)

def run_pipeline(spark):
    """
    Ejecuta el pipeline completo sobre una lista de archivos .txt CMAPSS.
    Procesa, filtra sensores irrelevantes y guarda los resultados en CSV.
    """

    # Directorios a validar
    directorios = [CARPETA_OUTPUT_CSV, CARPETA_OUTPUT_DATA_TEST]

    # Verificar si hay archivos en cualquiera de las carpetas
    for carpeta in directorios:
        if os.path.isdir(carpeta):
            archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
            if archivos:
                print(f"La carpeta '{carpeta}' contiene archivos. Pipeline NO se ejecutará.")
                logger.info(f"Pipeline detenido. Carpeta con contenido: {carpeta}")
                return None

    # Si ambas carpetas están vacías, se ejecuta el pipeline
    try:
        resultados = procesar_varios_archivos(spark, DATA_PATHS_TRAIN, CSV_OUTPUT)
        logger.info("Pipeline ejecutado correctamente sobre todos los archivos.")
    except Exception as e:
        logger.error(f"Error en el pipeline: {e}")
        print("Error en el pipeline. Revisar logs/pipeline.log para más detalles.")
        return None

    print("\nPipeline completado correctamente.")
    return resultados

