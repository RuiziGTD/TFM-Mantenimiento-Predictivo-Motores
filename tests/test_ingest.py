# TEST 2: Carga de datos inventados

from src.ingest.batch_ingest import procesar_varios_archivos
import pandas as pd
import tempfile, os, pytest


def test_procesar_varios_archivos_ok(tmp_path):
    data = " ".join(["1"] * 26) + "\n" + " ".join(["2"] * 26)

    path = tmp_path / "test.txt"
    path_csv = tmp_path / "csv"
    path_test = tmp_path / "test"
    path.write_text(data)

    resultados = procesar_varios_archivos(None, [str(path)], path_csv, path_test)

    assert isinstance(resultados, list)
    assert len(resultados) == 1
    assert isinstance(resultados[0], pd.DataFrame)
    assert resultados[0].shape[0] == 2
