from src.pipeline.pipeline import *
from src.modelo_ia.modelo_prueba_1 import *
from config import *
from src.processing.spark import *

open("logs/pipeline.log", "w").close()

if __name__ == "__main__":
    choice = None
    while choice not in ("y", "n"):
        choice = input(
            "¿Quieres usar spark? Se recomienda encarecidamente el uso de entorno Linux para el uso de Spark (y/n): "
        ).lower()
        if choice not in ("y", "n"):
            print("Caracter no reconocido, por favor responda usando 'y' en caso afirmativo o 'n' en caso negativo")

    spark = spark_init() if choice == "y" else None
    run_pipeline(spark)
    if spark:
        spark.stop()

    resultados = train_autoencoder_rul(
        "../output/train_FD002_filtrado.csv",
        "../output/data_test/test_FD002_filtrado.csv",
        "../data/raw_data/RUL_FD002.txt",
        encoding_dim=32,
        epochs=100,
    )

    print("MSE en test:", resultados["metrics"]["MSE"])
    print("R2 en test:", resultados["metrics"]["R2"])
