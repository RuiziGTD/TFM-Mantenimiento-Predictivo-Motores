from src.ingest.batch_ingest import load_batch
from src.utils.logger import get_logger
from src.processing.cleaning import *
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="environment/.env")

DATA_PATH_TRAIN_FD001 = os.getenv("DATA_PATH_TRAIN_FD001")
logger = get_logger(__name__)

def run_pipeline():
    
    # 1. Cargar dataset crudo
    try:
        df_raw = load_batch(DATA_PATH_TRAIN_FD001)
        logger.info("Dataset cargado correctamente.")
    except Exception as e:
        logger.error(f"Error en la carga de datos: {e}")
        print("Error en el pipeline. Revisar logs/pipeline.log para más detalles.")
        return

    # 2. Asignar nombres de columnas
    try:
        df_processed = assign_column_names(df_raw)
        logger.info("Asignación de nombres y limpieza completada.")
    except Exception as e:
        logger.error(f"Error al asignar nombres de columnas: {e}")
        print("Error en el pipeline. Revisar logs/pipeline.log para más detalles.")
        return

    # 3. Identificar sensores irrelevantes
    try:
        resultados = identificar_sensores_irrelevantes(df_processed)
        sensors_to_drop = resultados["sensors_to_drop"]
        sensors_to_keep = resultados["sensors_to_keep"]
        logger.info("Identificación de sensores irrelevantes completada.")
    except Exception as e:
        logger.error(f"Error al identificar sensores irrelevantes: {e}")
        print("Error en el pipeline durante la identificación de sensores irrelevantes.")
        return

    print("\nPipeline completado correctamente.")
    return {
        "df_processed": df_processed,
        "sensors_to_drop": sensors_to_drop,
        "sensors_to_keep": sensors_to_keep
    }

