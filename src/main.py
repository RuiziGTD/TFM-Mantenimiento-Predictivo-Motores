from src.pipeline.pipeline import *
from src.modelo_ia.modelo_1 import *
from src.modelo_ia.modelo_2 import *
from src.config import *
from src.processing.spark import *

open("logs/pipeline.log", "w").close()

if __name__ == "__main__":
    spark_choice = None
    while spark_choice not in ("y", "n"):
        spark_choice = input(
            "¿Quieres usar spark? Se recomienda encarecidamente el uso de entorno Linux para el uso de Spark (y/n): "
        ).lower()
        if spark_choice not in ("y", "n"):
            print(
                "Caracter no reconocido, por favor responda usando 'y' en caso afirmativo o 'n' en caso negativo"
            )
    
    eda_choice = input(
            "¿Quieres crear un EDA? Este se guardara en \"resultados_eda/\" (solo se creará en caso de realizar el filtrado) (Y/n): "
        ).lower()

    spark = spark_init() if spark_choice == "y" else None
    eda = "y" if eda_choice != "n" else None

    params = [spark, eda]

    run_pipeline(params)

    if spark:
        spark.stop()

    resultados = train_lstm_rul2(
        train_path=[
            "output/output_csv/train_FD001_filtrado.csv",
            "output/output_csv/train_FD002_filtrado.csv",
            "output/output_csv/train_FD003_filtrado.csv",
            "output/output_csv/train_FD004_filtrado.csv",
        ],
        test_path="output/data_test/test_FD002_filtrado.csv",
        rul_path="data/raw_data/RUL_FD002.txt",
        epochs=200,
    )

    m = resultados["metrics"]
    print(
        f"MSE: {m['MSE']:.2f}, RMSE: {m['RMSE']:.2f}, R2: {m['R2']:.3f}, NASA_Score: {m['NASA_Score']:.3f}"
    )

    # Acceder a las predicciones
    df_pred = resultados["predicciones"]
    print(df_pred.head())
