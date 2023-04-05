import importlib
import sys
from typing import Any
from app.config import settings


def resolve_dotted_path(path: str) -> Any:
    """Retrieves attribute (var, function, class, etc.) from module by
    dotted path.

    Example:
        from datetime.datetime import utcnow as default_utcnow
        utcnow = resolve_dotted_path('datetime.datetime.utcnow')
        assert utcnow == default_utcnow

    Args:
        path: dotted path to the attribute in module
    Returns
        Desired attribute or None
    """
    splitted = path.split(".")
    if len(splitted) <= 1:
        return importlib.import_module(path)
    module, attr = ".".join(splitted[:-1]), splitted[-1]
    module = importlib.import_module(module)
    return getattr(module, attr)


def get_logger() -> Any:
    """
    Gets logger that will be used throughout this whole library.
    First it finds and imports the logger, then if it can be configured
    using loguru-compatible config, it does so.

    Returns:
        desired logger (pre-configured if loguru)
    """
    lib_logger = resolve_dotted_path(settings.logger)

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
