from klovis.extraction.vl_extractor import VLExtractor
from klovis.exceptions import MissingAPIKeyError
from klovis.config.settings import Settings
import os


def test_vl_extractor_with_api_key(monkeypatch):
    """Test VLExtractor when API key is present."""
    # Mock Settings class method to have API key
    original_has_api_key = Settings.has_api_key
    monkeypatch.setattr(Settings, "has_api_key", classmethod(lambda cls: True))
    
    extractor = VLExtractor()
    
    data = [
        {"source": "test1.jpg", "content": "Image 1"},
        {"source": "test2.png", "content": "Image 2"},
    ]
    
    result = extractor.extract(data)
    
    assert len(result) == 2
    assert "extracted_text" in result[0]
    assert "test1.jpg" in result[0]["extracted_text"]
    
    # Restore original method
    monkeypatch.setattr(Settings, "has_api_key", original_has_api_key)


def test_vl_extractor_without_api_key(monkeypatch):
    """Test VLExtractor raises error when API key is missing."""
    # Mock Settings class method to not have API key
    original_has_api_key = Settings.has_api_key
    monkeypatch.setattr(Settings, "has_api_key", classmethod(lambda cls: False))
    
    try:
        extractor = VLExtractor()
        assert False, "Should raise MissingAPIKeyError"
    except MissingAPIKeyError:
        pass
    finally:
        # Restore original method
        monkeypatch.setattr(Settings, "has_api_key", original_has_api_key)

