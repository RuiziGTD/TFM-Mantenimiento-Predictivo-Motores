import pandas as pd
from src.utils.logger import get_logger  # Obtain logs
from src.processing.cleaning import identificar_sensores_irrelevantes_y_guardar

logger = get_logger(__name__)


def procesar_varios_archivos(
    spark, lista_rutas: list[str], output_dir: str = "../output"
) -> list[pd.DataFrame]:
    """
    Itera sobre una lista de rutas de archivos .txt, aplica el filtrado de sensores irrelevantes
    y guarda cada resultado como .csv en la carpeta de salida.
    Devuelve una lista de DataFrames filtrados.
    """
    resultados = []

    for ruta in lista_rutas:
        try:
            logger.info(f"Procesando archivo: {ruta}")
            df_filtrado = identificar_sensores_irrelevantes_y_guardar(
                spark, ruta, output_dir
            )
            resultados.append(df_filtrado)
        except Exception as e:
            logger.error(f"Error al procesar {ruta}: {e}")

    logger.info(f"Procesamiento completado para {len(resultados)} archivos.")
    return resultados
