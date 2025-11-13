"""
Logger configuration for Klovis.
Provides a structured, configurable logger for all modules.
"""

import logging
import sys
from klovis.config.settings import settings


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger instance for the given module."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Dynamically set log level from environment variable
        level = settings.LOG_LEVEL
        if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            level = "INFO"
        logger.setLevel(getattr(logging, level))

        logger.info(f"Logger initialized with level: {level}")

    return logger
