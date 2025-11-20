from src.pipeline.pipeline import run_pipeline
import pytest, os
import pandas as pd

# TEST 1: Testear la carga de datos con un dataset inventado

def test_run_pipeline(monkeypatch, tmp_path):
    file = tmp_path / "fake.csv"
    file.write_text(" ".join(["1"] * 26) + "\n" + " ".join(["2"] * 26))

    monkeypatch.setenv("DATA_PATH_TRAIN_FD001", str(file))
    monkeypatch.setattr(os, "listdir", lambda x: [])

    result1, result2 = run_pipeline(None)

    # run_pipeline devuelve una lista de DataFrames
    assert isinstance(result1, list)
    assert isinstance(result2, list)
    assert len(result1) > 0
    assert isinstance(result1[0], pd.DataFrame)
    assert all(
        col in result1[0].columns for col in ["unit_number", "time_in_cycles", "RUL"]
    )
