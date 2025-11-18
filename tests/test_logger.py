from klovis.utils.logger import get_logger
import logging


def test_get_logger():
    """Test logger creation."""
    logger = get_logger("test_module")
    
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_module"


def test_logger_has_handler():
    """Test that logger has a handler."""
    logger = get_logger("test_module_2")
    
    assert len(logger.handlers) > 0


def test_logger_level():
    """Test logger level setting."""
    logger = get_logger("test_module_3")
    
    # Should have a valid level
    assert logger.level in [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL
    ]

