from src.pipeline.pipeline import *
from src.processing.spark import *

open("logs/pipeline.log", "w").close()

if __name__ == "__main__":
    spark = spark_init()
    run_pipeline(spark)
    spark.stop()
