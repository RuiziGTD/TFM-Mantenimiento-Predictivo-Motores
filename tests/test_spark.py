from unittest.mock import patch, MagicMock
from src.processing.spark_utils import spark_data_lake, spark_init
import pytest

# TEST 9: Comprobar el correcto funcionamiento del inició de sesión Spark


def test_spark_init_integration():
    spark = spark_init()
    assert spark is not None
    assert spark.version  # Comprobación mínima
    spark.stop()


from src.config import PARQUET_OUTPUT

# TEST 10: Comprobar la creación de un datalake con un objeto simulando un dataframe spark


def test_spark_data_lake():
    # MagicMock sirve para simular un objeto que originalmente necesitaria el lanzamiento de un servicio
    # Hace el test más rapido y sin necesidad de usar Linux
    spark = MagicMock()
    spark_df = MagicMock()
    spark.createDataFrame.return_value = spark_df

    df = MagicMock()
    path_txt = "input/cars.txt"

    with patch("os.makedirs") as mock_makedirs, patch(
        "os.path.splitext", return_value=("cars", ".txt")
    ), patch("os.path.basename", return_value="cars.txt"), patch(
        "os.path.join", return_value=f"{PARQUET_OUTPUT}/cars_parquet"
    ):

        spark_data_lake(spark, df, path_txt)

        # Se llama a crear el DataFrame
        spark.createDataFrame.assert_called_once_with(df)

        # Se llama a crear la carpeta
        mock_makedirs.assert_called_once_with(PARQUET_OUTPUT, exist_ok=True)

        # Se escribe parquet
        spark_df.write.mode.return_value.parquet.assert_called_once_with(
            f"{PARQUET_OUTPUT}/cars_parquet"
        )
