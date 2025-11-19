from src.pipeline.pipeline import *
from src.modelo_ia.modelo_prueba_1 import *
from src.modelo_ia.modelo_prueba_3 import *
from src.config import *
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



resultados = train_lstm_rul(
    train_path=[
        "output/output_csv/train_FD001_filtrado.csv",
        "output/output_csv/train_FD002_filtrado.csv",
        "output/output_csv/train_FD003_filtrado.csv",
        "output/output_csv/train_FD004_filtrado.csv"
    ],
    test_path="output/data_test/test_FD002_filtrado.csv",
    rul_path="data/raw_data/RUL_FD002.txt",
    epochs=200
)

for dataset, m in resultados["metrics"].items():
    print(f"Dataset {dataset} -> MSE: {m['MSE']:.2f}, R2: {m['R2']:.3f}")


"""
resultados_fd002 = train_lstm_rul(
    train_path="../output/output_csv/train_FD002_filtrado.csv",
    test_path="../output/data_test/test_FD002_filtrado.csv",
    rul_path="../data/raw_data/RUL_FD002.txt",
    sequence_length=50,
    epochs=100
)

print("\nPredicciones FD002 (primeras filas):")
print(resultados_fd002["predicciones"].head())
"""