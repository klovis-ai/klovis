from klovis.merger.semantic_merger import SemanticMerger
from klovis.models import Chunk
import numpy as np


class MockEmbedder:
    """Mock embedder for testing."""
    
    def __init__(self, dimension=384):
        self.dimension = dimension
    
    def embed(self, texts):
        """Return random embeddings."""
        return [np.random.rand(self.dimension).tolist() for _ in texts]


def test_semantic_merger_basic():
    """Test basic semantic merging."""
    embedder = MockEmbedder()
    merger = SemanticMerger(
        embedder=embedder,
        max_size=1000,
        batch_size=5,
        distance_threshold=0.5
    )
    
    chunks = [
        Chunk(text="First chunk " * 10, metadata={"chunk_id": 0}),
        Chunk(text="Second chunk " * 10, metadata={"chunk_id": 1}),
        Chunk(text="Third chunk " * 10, metadata={"chunk_id": 2}),
    ]
    
    merged = merger.merge(chunks)
    
    assert len(merged) > 0
    assert all(isinstance(c, Chunk) for c in merged)
    assert all("type" in c.metadata for c in merged)
    assert all(c.metadata["type"] == "semantic" for c in merged)


def test_semantic_merger_empty():
    """Test merging empty list."""
    embedder = MockEmbedder()
    merger = SemanticMerger(embedder=embedder)
    
    merged = merger.merge([])
    assert merged == []


def test_semantic_merger_single_chunk():
    """Test merging single chunk."""
    embedder = MockEmbedder()
    merger = SemanticMerger(embedder=embedder, max_size=1000)
    
    chunks = [Chunk(text="Single chunk", metadata={"chunk_id": 0}), Chunk(text="Single chunk 2", metadata={"chunk_id": 1})]
    merged = merger.merge(chunks)
    
    assert len(merged) >= 1
    assert merged[0].text == "Single chunk"

