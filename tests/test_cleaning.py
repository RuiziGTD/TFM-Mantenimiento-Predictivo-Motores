import pytest
import pandas as pd
from src.processing.cleaning import assign_column_names, identificar_sensores_irrelevantes

# TEST 3: Para assign_column_names con un dataset de mentira
def test_assign_column_names_ok():
    # Simular dataset crudo con 26 columnas (5 + 21 sensores)
    data = [[i for i in range(26)] for _ in range(3)]
    df_raw = pd.DataFrame(data)

    df_named = assign_column_names(df_raw)

    # Validaciones
    assert isinstance(df_named, pd.DataFrame)
    assert len(df_named.columns) == 26
    assert "unit_number" in df_named.columns
    assert "T2" in df_named.columns
    assert "W32" in df_named.columns
    assert df_named.columns[0] == "unit_number"
    assert df_named.columns[-1] == "W32"


# TEST 4: Para identificar_sensores_irrelevantes con valores de desviación estandar simulados
def test_identificar_sensores_irrelevantes_ok():
    # Crear DataFrame con sensores, algunos sin variación
    data = {
        "unit_number": [1, 2, 3],
        "time_in_cycles": [1, 2, 3],
        "op_setting_1": [0.1, 0.2, 0.3],
        "op_setting_2": [0.4, 0.5, 0.6],
        "op_setting_3": [0.7, 0.8, 0.9],
        # sensores relevantes (varían)
        "T2": [1, 2, 3],
        "T24": [10, 20, 30],
        "T30": [5, 5, 5],     # <- sin variación
        "T50": [2, 3, 4],
        "P2": [1.0, 1.0, 1.0], # <- sin variación
        "P15": [2, 2.1, 2.2],
        "P30": [3, 4, 5],
        "Nf": [6, 7, 8],
        "Nc": [9, 10, 11],
        "epr": [1, 1, 1],     # <- sin variación
        "Ps30": [2, 3, 2.5],
        "phi": [0.1, 0.2, 0.3],
        "NRf": [100, 101, 99],
        "NRc": [200, 200, 200], # <- sin variación
        "BPR": [0.5, 0.6, 0.7],
        "farB": [0.8, 0.9, 1.0],
        "htBleed": [0.0, 0.0, 0.0], # <- sin variación
        "Nf_dmd": [5, 6, 7],
        "PCNfR_dmd": [7, 8, 9],
        "W31": [1, 2, 3],
        "W32": [1, 1, 1], # <- sin variación
    }
    df = pd.DataFrame(data)

    result = identificar_sensores_irrelevantes(df)

    # Comprobaciones básicas
    assert isinstance(result, dict)
    assert "df_train" in result
    assert "sensors_to_drop" in result
    assert "sensors_to_keep" in result

    drop = result["sensors_to_drop"]
    keep = result["sensors_to_keep"]

    # Debe detectar sensores con desviación estándar ~0
    assert "T30" in drop
    assert "P2" in drop
    assert "epr" in drop
    assert "NRc" in drop
    assert "htBleed" in drop
    assert "W32" in drop

    # Asegurar que los que varían se mantienen
    assert "T2" in keep
    assert "phi" in keep
    assert all(col not in result["df_train"].columns for col in drop)
