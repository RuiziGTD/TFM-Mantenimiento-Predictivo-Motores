# TEST 1: Testear la carga de datos con un dataset inventado

from src.pipeline.pipeline import run_pipeline
import pytest
import os

def test_run_pipeline(monkeypatch, tmp_path):
    # Simular variable de entorno
    fake_file = tmp_path / "fake.csv"
    fake_file.write_text("1 2 3\n4 5 6")
    monkeypatch.setenv("DATA_PATH_TRAIN_FD001", str(fake_file))

    result = run_pipeline()
    assert "df_processed" in result
    assert "sensors_to_drop" in result
    assert "sensors_to_keep" in result
