import logging
from pathlib import Path


def get_logger(name: str):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Formato uniforme
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para consola
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Handler para archivo
    fh = logging.FileHandler(logs_dir / "pipeline.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
