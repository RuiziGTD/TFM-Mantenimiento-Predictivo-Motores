# TEST 1: Testear la carga de datos con un dataset inventado

from src.pipeline.pipeline import run_pipeline
import pytest, os
import pandas as pd


def test_run_pipeline(monkeypatch, tmp_path):
    file = tmp_path / "fake.csv"
    file.write_text(" ".join(["1"] * 26) + "\n" + " ".join(["2"] * 26))

    monkeypatch.setenv("DATA_PATH_TRAIN_FD001", str(file))

    result = run_pipeline(None)

    # run_pipeline devuelve una lista de DataFrames
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], pd.DataFrame)
    assert all(col in result[0].columns for col in ["unit_number", "time_in_cycles", "RUL"])


