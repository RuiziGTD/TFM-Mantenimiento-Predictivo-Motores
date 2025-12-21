import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "api.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),  # Consola
        RotatingFileHandler(
            LOG_FILE,
            maxBytes=5_000_000,    # 5 MB
            backupCount=3
        )
    ]
)

def get_logger(name: str):
    return logging.getLogger(name)
