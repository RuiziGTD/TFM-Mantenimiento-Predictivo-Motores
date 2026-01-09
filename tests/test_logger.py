import logging
from pathlib import Path
from src.utils.logger import get_logger

# TEST 5: Test que comprueba la correcta creación de un archivo .log


def test_get_logger(tmp_path, monkeypatch):
    # Redirigir el directorio logs al temp
    monkeypatch.chdir(tmp_path)

    logger = get_logger("test")

    # 1. Nombre correcto
    assert logger.name == "test"

    # 2. Nivel INFO
    assert logger.level == logging.INFO

    # 3. Handlers correctos
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    assert file_handlers

    # 4. Archivo creado
    log_file = tmp_path / "logs" / "pipeline.log"
    assert log_file.exists()
