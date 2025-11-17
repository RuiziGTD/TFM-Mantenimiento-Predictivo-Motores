from pyspark.sql import SparkSession
from sklearn.preprocessing import StandardScaler
import pandas as pd
from src.utils.logger import get_logger
from src.config import PARQUET_OUTPUT
import os, sys

logger = get_logger(__name__)

def spark_init():

    try:
        spark = (
            SparkSession.builder
                .master("local[*]")
                .appName("Data Lake Motores")
                .getOrCreate()
        )
        spark

    except Exception:
        logger.error("Error al cargar la sesión Spark")
        raise

    return spark

def spark_data_lake(spark, df: pd.DataFrame, path_txt: str):

    spark_df = spark.createDataFrame(df)

    os.makedirs(PARQUET_OUTPUT, exist_ok=True)

    filename = os.path.splitext(os.path.basename(path_txt))[0] + "_parquet"
    output_path = os.path.join(PARQUET_OUTPUT, filename)

    spark_df.write.mode("overwrite").parquet(output_path)

    return

