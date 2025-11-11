# TEST 2: Carga de datos inventados

from src.ingest.batch_ingest import load_batch
import pandas as pd
import tempfile, os, pytest

def test_load_batch_ok():
    data = "1 2 3\n4 5 6"
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(data)
        path = f.name
    df = load_batch(path)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 3)
    os.remove(path)
