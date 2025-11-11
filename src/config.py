import os

# Base del proyecto (una carpeta arriba de src/)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # sube desde src/

# Carpeta donde están los datos
DATA_DIR = os.path.join(BASE_DIR, "data", "raw_data")

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

# Lista completa de rutas
DATA_PATHS_TRAIN = [
    DATA_PATH_TRAIN_FD001,
    DATA_PATH_TRAIN_FD002,
    DATA_PATH_TRAIN_FD003,
    DATA_PATH_TRAIN_FD004
]