from src.ingest.batch_ingest import load_batch
from src.utils.logger import get_logger
from src.processing.cleaning import assign_column_names

logger = get_logger(__name__)

def run_pipeline():

    # LOAD RAW DATAFRAME
    try:
        df_raw = load_batch("data/raw_data/train_FD001.txt")
    except Exception as e:
        logger.error(f"Error en la carga de datos")
        print("Error en el pipeline. Revisar logs/pipeline.log para más detalles.")

    try:
        df_processed = assign_column_names(df_raw)
    except Exception as e:
        logger.error(f"Error en el formateo y la limpieza de datos: {e}")
        print("Error en el pipeline. Revisar logs/pipeline.log para más detalles.")


