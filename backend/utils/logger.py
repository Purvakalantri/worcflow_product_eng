import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


# Project root = workflow-ai/
BASE_DIR = Path(__file__).resolve().parents[2]

# Logs directory = workflow-ai/logs/
LOG_DIR = BASE_DIR / "Backend" /"logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


LOG_FILE = LOG_DIR / "app.log"


def configure_logger() -> logging.Logger:
    logger = logging.getLogger("workflow_ai")

    # Prevent duplicate handlers if configure_logger() is called again
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s | %(message)s"
    )

    # File handler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = configure_logger()