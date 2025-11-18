from klovis.chunking.markdown_chunker import MarkdownChunker
from klovis.models import Chunk, Document


def test_markdown_chunker_basic():
    """Test basic markdown chunking by headings."""
    content = """# Title 1
Content for title 1.

## Subtitle 1.1
Content for subtitle 1.1.

## Subtitle 1.2
Content for subtitle 1.2.

# Title 2
Content for title 2.
"""
    doc = Document(source="test.md", content=content)
    
    chunker = MarkdownChunker(max_chunk_size=1000, overlap=50)
    chunks = chunker.chunk([doc])
    
    assert len(chunks) > 0
    assert all(isinstance(c, Chunk) for c in chunks)
    assert all("chunk_id" in c.metadata for c in chunks)
    assert all("type" in c.metadata for c in chunks)


def test_markdown_chunker_large_section():
    """Test that large sections are split."""
    content = """# Title
""" + "Content " * 500  # Very long content
    
    doc = Document(source="test.md", content=content)
    
    chunker = MarkdownChunker(max_chunk_size=100, overlap=20)
    chunks = chunker.chunk([doc])
    
    assert len(chunks) > 1
    assert all(len(c.text) <= 100 + 20 for c in chunks)  # Account for overlap


def test_markdown_chunker_no_headings():
    """Test chunking content without markdown headings."""
    content = "This is plain text without any markdown headings."
    doc = Document(source="test.md", content=content)
    
    chunker = MarkdownChunker(max_chunk_size=1000)
    chunks = chunker.chunk([doc])
    
    assert len(chunks) >= 1
    assert chunks[0].text.strip() == f"# Section\n{content}"

