# Chunkers API Reference

Complete API documentation for all chunker classes.

## SimpleChunker

Splits documents into fixed-size chunks with optional overlap.

### Class Definition

```python
class SimpleChunker(BaseChunker):
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        separators: List[str] | None = None,
        smart_overlap: bool = True,
    )
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chunk_size` | `int` | `1000` | Maximum characters per chunk |
| `chunk_overlap` | `int` | `100` | Characters to overlap between chunks |
| `separators` | `List[str]` | `None` | Preferred split points (ordered by priority) |
| `smart_overlap` | `bool` | `True` | Avoid cutting words in overlap region |

### Default Separators

If `separators` is `None`, uses:
```python
["\n\n", "\n", ". ", "? ", "! ", "; "]
```

### Methods

#### `chunk(documents: List[Document]) -> List[Chunk]`

Splits documents into chunks.

**Parameters:**
- `documents` (`List[Document]`): Documents to chunk

**Returns:**
- `List[Chunk]`: List of chunked documents

**Example:**
```python
chunker = SimpleChunker(chunk_size=500, chunk_overlap=50)
chunks = chunker.chunk(documents)
```

### Chunk Metadata

Generated chunks include:
- `chunk_id`: Sequential chunk identifier
- `source`: Source document path
- `length`: Character count of chunk text

---

## MarkdownChunker

Splits documents based on Markdown heading structure.

### Class Definition

```python
class MarkdownChunker(BaseChunker):
    def __init__(
        self,
        max_chunk_size: int = 2000,
        overlap: int = 200,
        merger: Optional[BaseMerger] = None,
    )
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_chunk_size` | `int` | `2000` | Maximum characters per chunk |
| `overlap` | `int` | `200` | Characters to overlap between chunks |
| `merger` | `BaseMerger` | `None` | Optional semantic merger for post-processing |

### Methods

#### `chunk(documents: List[Document]) -> List[Chunk]`

Splits documents by Markdown headings.

**Parameters:**
- `documents` (`List[Document]`): Documents to chunk

**Returns:**
- `List[Chunk]`: List of chunked documents

**Example:**
```python
chunker = MarkdownChunker(max_chunk_size=1500, overlap=150)
chunks = chunker.chunk(documents)
```

### How It Works

1. Splits content by Markdown headings (`#`, `##`, `###`, etc.)
2. Groups sections together up to `max_chunk_size`
3. If a section exceeds `max_chunk_size`, it's hard-split
4. Applies overlap between consecutive chunks

### Chunk Metadata

Generated chunks include:
- `chunk_id`: Sequential chunk identifier
- `source`: Source document path
- `length`: Character count
- `type`: `"markdown"` or `"markdown_hardsplit"`

### With Semantic Merger

```python
from klovis.merger import SemanticMerger

merger = SemanticMerger(embedder=embedder, max_size=4000)
chunker = MarkdownChunker(
    max_chunk_size=500,
    overlap=100,
    merger=merger,
)
chunks = chunker.chunk(documents)
```

---

## BaseChunker

Abstract base class for all chunkers.

### Class Definition

```python
class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, documents: List[Document]) -> List[Chunk]:
        pass
```

### Creating Custom Chunkers

```python
from klovis.base import BaseChunker
from klovis.models import Document, Chunk
from typing import List

class CustomChunker(BaseChunker):
    def chunk(self, documents: List[Document]) -> List[Chunk]:
        chunks = []
        for doc in documents:
            # Your chunking logic
            chunk = Chunk(
                text=doc.content,
                metadata={"chunk_id": 0, "source": doc.source}
            )
            chunks.append(chunk)
        return chunks
```

