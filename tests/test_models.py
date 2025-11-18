from klovis.models import Document, Chunk, KlovisBaseModel
import json


def test_document_creation():
    """Test Document model creation."""
    doc = Document(
        source="test.txt",
        content="Test content",
        metadata={"key": "value"}
    )
    
    assert doc.source == "test.txt"
    assert doc.content == "Test content"
    assert doc.metadata == {"key": "value"}


def test_chunk_creation():
    """Test Chunk model creation."""
    chunk = Chunk(
        text="Chunk text",
        metadata={"chunk_id": 0}
    )
    
    assert chunk.text == "Chunk text"
    assert chunk.metadata == {"chunk_id": 0}


def test_document_to_dict():
    """Test Document serialization to dict."""
    doc = Document(source="test.txt", content="Content")
    doc_dict = doc.to_dict()
    
    assert isinstance(doc_dict, dict)
    assert doc_dict["source"] == "test.txt"
    assert doc_dict["content"] == "Content"


def test_chunk_to_json():
    """Test Chunk serialization to JSON."""
    chunk = Chunk(text="Text", metadata={"id": 1})
    json_str = chunk.to_json()
    
    assert isinstance(json_str, str)
    parsed = json.loads(json_str)
    assert parsed["text"] == "Text"
    assert parsed["metadata"]["id"] == 1


def test_document_default_metadata():
    """Test Document with default empty metadata."""
    doc = Document(source="test.txt", content="Content")
    
    assert doc.metadata == {}


def test_chunk_default_metadata():
    """Test Chunk with default empty metadata."""
    chunk = Chunk(text="Text")
    
    assert chunk.metadata == {}

