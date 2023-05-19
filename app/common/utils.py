"Common utilities module"

import sys
from pydoc import locate
from typing import Any

from app.config import settings


def get_logger() -> Any:
    """
    Gets logger that will be used throughout this whole library.
    First it finds and imports the logger, then if it can be configured
    using loguru-compatible config, it does so.

    Returns:
        desired logger (pre-configured if loguru)
    """
    lib_logger = locate(settings.logger)

    if hasattr(lib_logger, "configure"):
        logger_config = {
            "handlers": [
                {
                    "sink": sys.stdout,
                    "level": settings.log_level,
                    "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
                    " | <level>{level: <8}</level> | "
                    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
                    "<cyan>{line}</cyan> -"
                    " <level>{message}</level>",
                }
            ]
        }
        lib_logger.configure(**logger_config)

    return lib_logger


logger = get_logger()
