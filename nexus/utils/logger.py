"""Logging Configuration"""

import logging
import logging.handlers
from pathlib import Path


def setup_logger(name: str, log_level: str = "INFO", log_file: str = "logs/nexus.log") -> logging.Logger:
    """Setup logger with file and console output"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if logger.hasHandlers():
        return logger

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        fh = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5
        )
        fh.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    except:
        fh = None

    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    if fh:
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
