# Chunking Guide

Chunking divides documents into smaller, manageable pieces suitable for indexing and retrieval.

## Overview

Klovis provides two main chunking strategies:

- **SimpleChunker**: Size-based chunking with overlap
- **MarkdownChunker**: Structure-aware chunking based on Markdown headings

## SimpleChunker

Splits documents into fixed-size chunks with optional overlap.

### Basic Usage

```python
from klovis.chunking import SimpleChunker
from klovis.models import Document

doc = Document(
    source="text.txt",
    content="Your long document text here... " * 100
)

chunker = SimpleChunker(
    chunk_size=1000,  # Characters per chunk
    chunk_overlap=100,  # Overlap between chunks
    smart_overlap=True,  # Avoid word breaks
)

chunks = chunker.chunk([doc])
print(f"Created {len(chunks)} chunks")
```

### Parameters

- `chunk_size` (int): Maximum characters per chunk (default: 1000)
- `chunk_overlap` (int): Characters to overlap between chunks (default: 100)
- `separators` (List[str]): Preferred split points, ordered by priority
- `smart_overlap` (bool): Avoid cutting words in overlap region (default: True)

### Default Separators

The default separator priority is:
1. `\n\n` - Paragraph breaks
2. `\n` - Line breaks
3. `. ` - Sentence endings
4. `? `, `! ` - Question/exclamation marks
5. `; ` - Semicolons

### Example

```python
chunker = SimpleChunker(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". "],  # Custom separators
    smart_overlap=True,
)

chunks = chunker.chunk(documents)
```

## MarkdownChunker

Splits documents based on Markdown heading structure.

### Basic Usage

```python
from klovis.chunking import MarkdownChunker

markdown_content = """# Introduction
Content here.

## Section 1
More content.

## Section 2
Even more content.
"""

doc = Document(source="doc.md", content=markdown_content)

chunker = MarkdownChunker(
    max_chunk_size=2000,  # Max size per chunk
    overlap=200,  # Overlap between chunks
)

chunks = chunker.chunk([doc])
```

### Parameters

- `max_chunk_size` (int): Maximum characters per chunk (default: 2000)
- `overlap` (int): Characters to overlap between chunks (default: 200)
- `merger` (BaseMerger, optional): Optional semantic merger for post-processing

### How It Works

1. Splits content by Markdown headings (`#`, `##`, `###`, etc.)
2. Groups sections together up to `max_chunk_size`
3. If a section exceeds `max_chunk_size`, it's hard-split
4. Applies overlap between consecutive chunks

### With Semantic Merger

You can combine MarkdownChunker with SemanticMerger:

```python
from klovis.chunking import MarkdownChunker
from klovis.merger import SemanticMerger

# Create merger (requires embedder)
merger = SemanticMerger(embedder=embedder, max_size=4000)

# Use in chunker
chunker = MarkdownChunker(
    max_chunk_size=500,
    overlap=100,
    merger=merger,  # Merge semantically similar chunks
)

chunks = chunker.chunk(documents)
```

## Choosing a Chunking Strategy

### Use SimpleChunker when:
- Documents don't have clear structure
- You need consistent chunk sizes
- Simple size-based splitting is sufficient
- Processing speed is important

### Use MarkdownChunker when:
- Documents have Markdown structure
- You want to preserve semantic sections
- Headings indicate logical boundaries
- Structure-aware chunking improves quality

## Chunk Metadata

All chunks include metadata:

```python
chunk.metadata = {
    "chunk_id": 0,  # Sequential ID
    "source": "doc.txt",  # Source document
    "length": 500,  # Chunk length
    "type": "simple"  # Chunk type
}
```

## Best Practices

1. **Choose appropriate size**: Balance between too small (fragmented) and too large (context loss)
2. **Use overlap**: Overlap helps preserve context at chunk boundaries
3. **Respect structure**: Use MarkdownChunker for structured documents
4. **Test chunk quality**: Inspect chunks to ensure they make sense
5. **Consider downstream use**: Chunk size affects embedding and retrieval quality

## Common Patterns

### Small Chunks for Embeddings

```python
chunker = SimpleChunker(
    chunk_size=500,  # Smaller for better embedding quality
    chunk_overlap=50,
)
```

### Large Chunks for Context

```python
chunker = SimpleChunker(
    chunk_size=2000,  # Larger for more context
    chunk_overlap=200,
)
```

### Structure-Aware Chunking

```python
chunker = MarkdownChunker(
    max_chunk_size=1500,
    overlap=150,
)
```

## Custom Chunkers

Create custom chunkers by inheriting from `BaseChunker`:

```python
from klovis.base import BaseChunker
from klovis.models import Document, Chunk
from typing import List

class CustomChunker(BaseChunker):
    def chunk(self, documents: List[Document]) -> List[Chunk]:
        chunks = []
        for doc in documents:
            # Your chunking logic here
            chunk = Chunk(
                text=doc.content[:500],
                metadata={"chunk_id": 0, "source": doc.source}
            )
            chunks.append(chunk)
        return chunks
```

## Next Steps

- Learn about [Merging](merging.md) to combine similar chunks
- See [API Reference](../api/chunkers.md) for complete API documentation
- Check [Examples](../examples/) for chunking patterns

