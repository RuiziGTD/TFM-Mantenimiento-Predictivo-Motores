from src.pipeline.pipeline import *
from src.processing.spark import *

open("logs/pipeline.log", "w").close()

if __name__ == "__main__":
    choice = ""

    while choice not in ("y", "n"):
        choice = input(
            "¿Quieres usar spark? Se recomienda encarecidamente el uso de entorno Linux para el uso de Spark (y/n): "
        ).lower()
        if choice not in ("y", "n"):
            print(
                "Caracter no reconocido, por favor responda usando 'y' en caso afirmativo o 'n' en caso negativo"
            )

    spark = spark_init() if choice == "y" else None

    run_pipeline(spark)
    if spark:
        spark.stop()
