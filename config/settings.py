"""
Klovis configuration module.
Handles environment variables, API key validation, and logging settings.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from klovis.exceptions import MissingAPIKeyError

# Load environment variables (from project root if needed)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    """Global configuration manager for Klovis."""

    KLOVIS_API_KEY: str | None = os.getenv("KLOVIS_API_KEY")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    @classmethod
    def require_api_key(cls):
        """Ensure a valid Klovis API key is available."""
        if not cls.KLOVIS_API_KEY or cls.KLOVIS_API_KEY.strip() == "":
            raise MissingAPIKeyError(
                "Klovis API key is missing. Please set 'KLOVIS_API_KEY' in your environment variables."
            )

    @classmethod
    def has_api_key(cls) -> bool:
        """Return True if a Klovis API key is set."""
        return bool(cls.KLOVIS_API_KEY and cls.KLOVIS_API_KEY.strip())


settings = Settings()
