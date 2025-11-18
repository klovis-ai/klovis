from klovis.exceptions import (
    KlovisError,
    MissingAPIKeyError,
    InvalidDataError,
    ProcessingError,
    ModuleDependencyError
)


def test_klovis_error_base():
    """Test base KlovisError exception."""
    error = KlovisError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_missing_api_key_error():
    """Test MissingAPIKeyError."""
    error = MissingAPIKeyError("API key missing")
    assert isinstance(error, KlovisError)
    assert str(error) == "API key missing"


def test_invalid_data_error():
    """Test InvalidDataError."""
    error = InvalidDataError("Invalid data format")
    assert isinstance(error, KlovisError)
    assert str(error) == "Invalid data format"


def test_processing_error():
    """Test ProcessingError."""
    error = ProcessingError("Processing failed")
    assert isinstance(error, KlovisError)
    assert str(error) == "Processing failed"


def test_module_dependency_error():
    """Test ModuleDependencyError."""
    error = ModuleDependencyError("Module not found")
    assert isinstance(error, KlovisError)
    assert str(error) == "Module not found"

