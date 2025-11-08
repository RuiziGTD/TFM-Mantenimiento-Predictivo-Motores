from src.utils.logger import get_logger  # Obtain logs
import pandas as pd

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


"""
Carga un dataset CMAPSS de la NASA, identifica sensores irrelevantes 
mediante la desviación estándar y devuelve los sensores útiles.
"""
def identificar_sensores_irrelevantes(df_train: pd.DataFrame):
    sensor_columns = [
        "T2", "T24", "T30", "T50", "P2", "P15",
        "P30", "Nf", "Nc", "epr", "Ps30", "phi",
        "NRf", "NRc", "BPR", "farB", "htBleed",
        "Nf_dmd", "PCNfR_dmd", "W31", "W32"
    ]

    sensor_std = df_train[sensor_columns].std()
    logger.info("Desviación estándar de los sensores:\n" + sensor_std.to_string())

    sensors_to_drop = sensor_std[sensor_std < 0.01].index.tolist()
    sensors_to_keep = [col for col in sensor_columns if col not in sensors_to_drop]

    logger.info(f"Sensores a descartar ({len(sensors_to_drop)}): {sensors_to_drop}")
    logger.info(f"Sensores a conservar ({len(sensors_to_keep)}): {sensors_to_keep}")

    df_train_filtered = df_train.drop(columns=sensors_to_drop)

    return {
        "df_train": df_train_filtered,
        "sensors_to_drop": sensors_to_drop,
        "sensors_to_keep": sensors_to_keep
    }