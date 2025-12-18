from pyspark.sql import SparkSession
from sklearn.preprocessing import StandardScaler
import pandas as pd
from utils.logger import get_logger
from config import PARQUET_OUTPUT
import os, sys

logger = get_logger(__name__)


def spark_init():

    try:
        spark = (
            SparkSession.builder.master("local[*]")
            .appName("Data Lake Motores")
            .getOrCreate()
        )
        spark

    except Exception:
        logger.error("Error al cargar la sesión Spark")
        raise

    return spark


def scale_group(group, sensor_cols):
    """Escala los sensores de un motor usando StandardScaler"""
    scaler = StandardScaler()
    group[sensor_cols] = scaler.fit_transform(group[sensor_cols])
    return group


def normalize_per_engine(spark, df: pd.DataFrame):
    """Normalizar los valores de los sensores por motor, para facilitar el entendimiento del modelo"""
    sensor_columns = df.columns[5:]  # Los sensores empiezan en la columna 6
    # Aplica la normalización por motor
    df_scaled = df.groupby("unit_number").apply(
        lambda g: scale_group(g, sensor_columns)
    )

    # Convierte a Spark DataFrame
    spark_df = spark.createDataFrame(df_scaled)
    return spark_df


def spark_data_lake(spark, df: pd.DataFrame, path_txt: str):

    spark_df = spark.createDataFrame(df)

    os.makedirs(PARQUET_OUTPUT, exist_ok=True)

    filename = os.path.splitext(os.path.basename(path_txt))[0] + "_parquet"
    output_path = os.path.join(PARQUET_OUTPUT, filename)

    spark_df.write.mode("overwrite").parquet(output_path)

    return
