import logging
import sys
from pathlib import Path


def setup_logger(
    level=logging.INFO,
    name=__name__,
    log_file: str | Path = None
) -> logging.Logger:
    """Настройки логгирования."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s %(name)s [%(levelname)s] %(message)s',
        datefmt='%d.%m.%Y %H:%M'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
