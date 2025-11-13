from src.utils.logger import get_logger  # Obtain logs
import pandas as pd
import os

logger = get_logger(__name__)

def assign_column_names(df: pd.DataFrame) -> pd.DataFrame:

    # Definir los tipos de sensores. Información del paper de la NASA
    sensor_names = {
    1: "T2", 2: "T24", 3: "T30", 4: "T50", 5: "P2", 6: "P15",
    7: "P30", 8: "Nf", 9: "Nc", 10: "epr", 11: "Ps30", 12: "phi",
    13: "NRf", 14: "NRc", 15: "BPR", 16: "farB", 17: "htBleed",
    18: "Nf_dmd", 19: "PCNfR_dmd", 20: "W31", 21: "W32"
    }

    # Definir
    cols = [
        "unit_number", "time_in_cycles", "op_setting_1", "op_setting_2", "op_setting_3",
        *sensor_names.values()
    ]
    df.columns = cols
    logger.info(f"Asignados {len(cols)} nombres de columnas al dataset.")
    logger.info(f"Mostrando vista de la tabla con valores de columnas asignadas")
    logger.info(f"Vista previa del dataset:\n{df.head().to_string(index=False)}")
    return df


def identificar_sensores_irrelevantes_y_guardar(path_txt: str, output_dir: str = "../output") -> pd.DataFrame:
    # Cargar el archivo .txt
    df_raw = pd.read_csv(path_txt, sep=" ", header=None)
    df_raw.dropna(axis=1, how="all", inplace=True)  # Eliminar columnas vacías por separadores extra

    # Asignar nombres de columnas
    df_named = assign_column_names(df_raw)

    # Identificar sensores irrelevantes
    sensor_columns = df_named.columns[5:]  # Los sensores empiezan en la columna 5
    sensor_std = df_named[sensor_columns].std()
    sensors_to_drop = sensor_std[sensor_std < 0.01].index.tolist()
    df_filtered = df_named.drop(columns=sensors_to_drop)

    # Añadir columna RUL
    df_filtered = calcular_rul(df_filtered)

    # Guardar el resultado
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.splitext(os.path.basename(path_txt))[0] + "_filtrado.csv"
    output_path = os.path.join(output_dir, filename)
    df_filtered.to_csv(output_path, index=False)

    logger.info(f"Archivo filtrado guardado en: {output_path}")
    logger.info(f"Sensores eliminados ({len(sensors_to_drop)}): {sensors_to_drop}")
    return 

def procesar_varios_archivos_txt(lista_rutas: list[str], output_dir: str = "../output") -> list[pd.DataFrame]:
    """
    Itera sobre una lista de rutas de archivos .txt, aplica el filtrado de sensores irrelevantes
    y guarda cada resultado como .csv en la carpeta de salida.
    Devuelve una lista de DataFrames filtrados.
    """
    resultados = []

    for ruta in lista_rutas:
        try:
            logger.info(f"Procesando archivo: {ruta}")
            df_filtrado = identificar_sensores_irrelevantes_y_guardar(ruta, output_dir)
            resultados.append(df_filtrado)
        except Exception as e:
            logger.error(f"Error al procesar {ruta}: {e}")

    logger.info(f"Procesamiento completado para {len(resultados)} archivos.")
    return resultados

def calcular_rul(df: pd.DataFrame) -> pd.DataFrame:
    """
    Añade la columna 'RUL' al DataFrame de entrenamiento.
    Calcula el RUL como la diferencia entre el ciclo final y el ciclo actual.
    """
    max_cycles = df.groupby("unit_number")["time_in_cycles"].max()
    df = df.merge(max_cycles.rename("max_cycle"), on="unit_number")
    df["RUL"] = df["max_cycle"] - df["time_in_cycles"]
    df.drop(columns=["max_cycle"], inplace=True)
    logger.info("Columna RUL añadida correctamente al dataset.")
    return df