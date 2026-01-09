import pandas as pd
from src.utils.logger import get_logger  # Obtain logs
from src.processing.cleaning import *

logger = get_logger(__name__)


def procesar_varios_archivos(
    params,
    lista_rutas: list[str],
    CARPETA_OUTPUT_CSV: str,
    CARPETA_OUTPUT_DATA_TEST: str,
) -> list[pd.DataFrame]:
    """
    Itera sobre una lista de rutas de archivos .txt, aplica el filtrado de sensores irrelevantes
    y guarda cada resultado en la carpeta correcta (train → CARPETA_OUTPUT_CSV, test → CARPETA_OUTPUT_DATA_TEST).
    Devuelve una lista de DataFrames filtrados.
    """

    resultados = []

    for ruta in lista_rutas:
        try:
            logger.info(f"Procesando archivo: {ruta}")
            df_filtrado = identificar_sensores_irrelevantes_y_guardar(
                params, ruta, CARPETA_OUTPUT_CSV, CARPETA_OUTPUT_DATA_TEST
            )
            resultados.append(df_filtrado)

        except Exception as e:
            logger.error(f"Error al procesar {ruta}: {e}")
            raise

    logger.info(f"Procesamiento completado para {len(resultados)} archivos.")
    return resultados
