import pandas as pd
from src.utils.logger import get_logger  # Obtain logs

logger = get_logger(__name__)

def load_batch(input_path: str) -> pd.DataFrame:
    logger.info(f"Cargando datos desde {input_path}")
    try:
        df = pd.read_csv(input_path, 
                         sep='\s+', 
                         header=None)
    except FileNotFoundError:
        logger.error(f"No se encontró el archivo: {input_path}")
        raise ValueError(f"El archivo {input_path} está vacío o corrupto.") from None
    except Exception as e: 
        logger.error(f"Error desconocido al cargar los datos")
        raise ValueError(f"Error desconocido al cargar los datos") from None

    if df.empty:
        logger.error("El dataset está vacío.")
        raise ValueError("El dataset está vacío")

    logger.info(f"{len(df)} filas cargadas correctamente")
    logger.info(f"Vista previa del dataset:\n{df.head().to_string(index=False)}")

    return df
