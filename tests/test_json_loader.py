from klovis.loaders.json_loader import JSONLoader
from klovis.models import Document
import tempfile
import os
import json


def test_json_loader_dict():
    """Test loading JSON with dictionary structure."""
    data = {"content": "This is test content"}
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name
    
    try:
        loader = JSONLoader(path=temp_path, text_field="content")
        docs = loader.load()
        
        assert len(docs) == 1
        assert isinstance(docs[0], Document)
        assert docs[0].content == "This is test content"
        assert docs[0].source == temp_path
    finally:
        os.unlink(temp_path)


def test_json_loader_list():
    """Test loading JSON with list structure."""
    data = [
        {"content": "First item"},
        {"content": "Second item"},
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name
    
    try:
        loader = JSONLoader(path=temp_path, text_field="content")
        docs = loader.load()
        
        assert len(docs) == 2
        assert docs[0].content == "First item"
        assert docs[1].content == "Second item"
    finally:
        os.unlink(temp_path)


def test_json_loader_custom_field():
    """Test loading JSON with custom text field."""
    data = {"text": "Custom field content"}
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name
    
    try:
        loader = JSONLoader(path=temp_path, text_field="text")
        docs = loader.load()
        
        assert len(docs) == 1
        assert docs[0].content == "Custom field content"
    finally:
        os.unlink(temp_path)


def test_json_loader_not_found():
    """Test error handling for non-existent file."""
    loader = JSONLoader(path="/file42.json")
    
    try:
        loader.load()
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass

