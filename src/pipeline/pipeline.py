from src.utils.logger import get_logger
from src.ingest.batch_ingest import *
from dotenv import load_dotenv
from src.config import *
from src.processing.cleaning import *
import os

load_dotenv(dotenv_path="environment/.env")
logger = get_logger(__name__)


def run_pipeline(spark):
    """
    Ejecuta el pipeline completo sobre TRAIN y TEST.
    Procesa y guarda en carpetas correspondientes.
    """

    # Directorios de salida
    directorios = [CARPETA_OUTPUT_CSV, CARPETA_OUTPUT_DATA_TEST]

    # Verificar si hay archivos en alguna carpeta de salida
    for carpeta in directorios:
        if os.path.isdir(carpeta):
            archivos = [f for f in os.listdir(carpeta)
                        if os.path.isfile(os.path.join(carpeta, f))]
            if archivos:
                print(f"La carpeta '{carpeta}' contiene archivos. Pipeline NO se ejecutará.")
                logger.info(f"Pipeline detenido. Carpeta con contenido: {carpeta}")
                return None

    # ----------------------
    # PROCESAR TRAIN
    # ----------------------
    try:
        resultados_train = procesar_varios_archivos(
            spark,
            DATA_PATHS_TRAIN,
            CARPETA_OUTPUT_CSV,
            CARPETA_OUTPUT_DATA_TEST
        )
        logger.info("Pipeline ejecutado correctamente sobre todos los archivos TRAIN.")
    except Exception as e:
        logger.error(f"Error en el pipeline TRAIN: {e}")
        print("Error en pipeline TRAIN. Revisar logs.")
        return None

    # ----------------------
    # PROCESAR TEST
    # ----------------------
    rutas_test = [
        ruta for ruta in DATA_PATHS_TEST
        if isinstance(ruta, str) and "test" in ruta.lower() and ruta.lower().endswith(".txt")
    ]

    try:
        resultados_test = procesar_varios_archivos(
            spark,
            rutas_test,
            CARPETA_OUTPUT_CSV,
            CARPETA_OUTPUT_DATA_TEST
        )
        logger.info("Pipeline ejecutado correctamente sobre todos los archivos TEST.")
    except Exception as e:
        logger.error(f"Error en pipeline TEST: {e}")
        print("Error en pipeline TEST. Revisar logs.")
        return None

    print("\nPipeline completado correctamente.")
    return resultados_train, resultados_test

