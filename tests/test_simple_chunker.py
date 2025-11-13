from klovis.chunking.simple_chunker import SimpleChunker
from klovis.models import Chunk, Document

def test_simple_chunker_basic():
    text = "This is a long text. " * 100
    doc = Document(source="test.txt", content=text)

    chunker = SimpleChunker(chunk_size=200, chunk_overlap=50)
    chunks = chunker.chunk([doc])

    assert len(chunks) > 1
    assert all(isinstance(c, Chunk) for c in chunks)
    assert all("chunk_id" in c.metadata for c in chunks)
    assert chunks[0].metadata.get("source") == "test.txt"
