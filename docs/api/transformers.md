# Transformers API Reference

Complete API documentation for transformer classes.

## MarkdownTransformer

Converts chunks into Markdown-formatted output.

### Class Definition

```python
class MarkdownTransformer(BaseTransformer):
    def __init__(self, include_metadata: bool = True)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_metadata` | `bool` | `True` | Include metadata in Markdown output |

### Methods

#### `transform(chunks: List[Chunk]) -> List[Dict]`

Transforms chunks to Markdown format.

**Parameters:**
- `chunks` (`List[Chunk]`): Chunks to transform

**Returns:**
- `List[Dict]`: List of dictionaries with `source`, `chunk_id`, and `markdown` keys

**Output Format:**
```python
[
    {
        "source": "doc.txt",
        "chunk_id": 0,
        "markdown": "## Source: `doc.txt`\n\n**Metadata:**\n- **chunk_id**: 0\n\n**Content:**\n\nContent here\n---\n"
    },
    ...
]
```

**Example:**
```python
from klovis.transforming import MarkdownTransformer

transformer = MarkdownTransformer(include_metadata=True)
markdown_chunks = transformer.transform(chunks)
```

### With Metadata

```python
transformer = MarkdownTransformer(include_metadata=True)
output = transformer.transform(chunks)
# Includes all metadata in Markdown format
```

### Without Metadata

```python
transformer = MarkdownTransformer(include_metadata=False)
output = transformer.transform(chunks)
# Only includes content, no metadata
```

---

## BaseTransformer

Abstract base class for all transformers.

### Class Definition

```python
class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, chunks: List[Chunk]) -> List[Dict]:
        pass
```

### Creating Custom Transformers

```python
from klovis.base import BaseTransformer
from klovis.models import Chunk
from typing import List, Dict

class CustomTransformer(BaseTransformer):
    def transform(self, chunks: List[Chunk]) -> List[Dict]:
        results = []
        for chunk in chunks:
            results.append({
                "id": chunk.metadata.get("chunk_id"),
                "text": chunk.text,
                "custom_format": "...",
            })
        return results
```

