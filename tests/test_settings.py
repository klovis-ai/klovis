from klovis.config.settings import settings
import os


def test_settings_exists():
    """Test that settings object exists."""
    assert settings is not None


def test_settings_log_level():
    """Test LOG_LEVEL setting."""
    # Should have a log level attribute
    assert hasattr(settings, "LOG_LEVEL")
    assert settings.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] or settings.LOG_LEVEL is None

