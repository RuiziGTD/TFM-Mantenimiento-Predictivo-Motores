from src.pipeline.pipeline import *
from src.modelo_ia.modelo_prueba_1 import *
from config import *

open("logs/pipeline.log", "w").close()

if __name__ == "__main__":
    #run_pipeline()

    resultados = train_autoencoder_rul(
        "../output/train_FD002_filtrado.csv",
        "../output/data_test/test_FD002_filtrado.csv",
        "../data/raw_data/RUL_FD002.txt",
        encoding_dim=32,
        epochs=100
    )

    print("MSE en test:", resultados["metrics"]["MSE"])
    print("R2 en test:", resultados["metrics"]["R2"])