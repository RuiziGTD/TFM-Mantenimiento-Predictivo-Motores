import os

# Base del proyecto (una carpeta arriba de src/)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # sube desde src/

# Carpeta donde están los datos
DATA_DIR = os.path.join(BASE_DIR, "data", "raw_data")

# Carpeta donde están los datos filtrados csv
DATA_DIR_FILTRADO = os.path.join(BASE_DIR, "output")

CARPETA_OUTPUT_CSV = os.path.join(BASE_DIR, "output/output_csv")
CARPETA_OUTPUT_DATA_TEST = os.path.join(BASE_DIR, "output/data_test")

# Rutas individuales
DATA_PATH_TRAIN_FD001 = os.path.join(DATA_DIR, "train_FD001.txt")
DATA_PATH_TRAIN_FD002 = os.path.join(DATA_DIR, "train_FD002.txt")
DATA_PATH_TRAIN_FD003 = os.path.join(DATA_DIR, "train_FD003.txt")
DATA_PATH_TRAIN_FD004 = os.path.join(DATA_DIR, "train_FD004.txt")

DATA_PATH_TEST_FD001 = os.path.join(DATA_DIR, "test_FD001.txt")
DATA_PATH_TEST_FD002 = os.path.join(DATA_DIR, "test_FD002.txt")
DATA_PATH_TEST_FD003 = os.path.join(DATA_DIR, "test_FD003.txt")
DATA_PATH_TEST_FD004 = os.path.join(DATA_DIR, "test_FD004.txt")

DATA_PATH_RUL_FD001 = os.path.join(DATA_DIR, "RUL_FD001.txt")
DATA_PATH_RUL_FD002 = os.path.join(DATA_DIR, "RUL_FD002.txt")
DATA_PATH_RUL_FD003 = os.path.join(DATA_DIR, "RUL_FD003.txt")
DATA_PATH_RUL_FD004 = os.path.join(DATA_DIR, "RUL_FD004.txt")

# Lista completa de rutas train
DATA_PATHS_TRAIN = [
    DATA_PATH_TRAIN_FD001,
    DATA_PATH_TRAIN_FD002,
    DATA_PATH_TRAIN_FD003,
    DATA_PATH_TRAIN_FD004
]

# Lista completa de rutas
DATA_PATHS_TEST = [
    DATA_PATH_TEST_FD001,
    DATA_PATH_TEST_FD002,
    DATA_PATH_TEST_FD003,
    DATA_PATH_TEST_FD004
]


# ENTRENAMIENTO PRUEBA
DATA_PATH_TRAIN_FD002_PRUEBA = os.path.join(DATA_DIR_FILTRADO, "train_FD002_filtrado.csv")
DATA_PATH_TRAIN_FD004_PRUEBA = os.path.join(DATA_DIR_FILTRADO, "train_FD004_filtrado.csv")

# 2 y 4
DATA_PATHS_ENTRENAMIENTO_PRUEBA = [
    DATA_PATH_TRAIN_FD002_PRUEBA,
    DATA_PATH_TRAIN_FD004_PRUEBA
]

CARPETA_OUTPUT = os.path.join(BASE_DIR, "../output")


CSV_OUTPUT = "output/output_csv"
PARQUET_OUTPUT = "output/output_parquet"