from klovis.loaders.document_loader import DocumentLoader
from klovis.models import Document

def test_loader_basic():
    loader = DocumentLoader()
    docs = loader.load(["test.txt"])

    assert len(docs) == 1
    assert isinstance(docs[0], Document)
    assert docs[0].source == "test.txt"
    assert "Loaded content" in docs[0].content
