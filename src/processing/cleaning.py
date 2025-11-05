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
