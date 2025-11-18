# Metadata API Reference

Complete API documentation for metadata generators.

## MetadataGenerator

Generates basic metadata for chunks.

### Class Definition

```python
class MetadataGenerator(BaseMetadataGenerator):
    def generate(self, chunks: List[Chunk]) -> List[Chunk]
```

### Methods

#### `generate(chunks: List[Chunk]) -> List[Chunk]`

Generates metadata for chunks.

**Parameters:**
- `chunks` (`List[Chunk]`): Chunks to enrich

**Returns:**
- `List[Chunk]`: Chunks with added metadata

**Generated Metadata:**
- `length`: Character count of chunk text
- `tags`: List of tags (default: `["example"]`)

**Example:**
```python
from klovis.metadata.metadata_generator import MetadataGenerator

generator = MetadataGenerator()
enriched = generator.generate(chunks)
```

**Note:** Preserves existing metadata in chunks.

---

## BaseMetadataGenerator

Abstract base class for all metadata generators.

### Class Definition

```python
class BaseMetadataGenerator(ABC):
    @abstractmethod
    def generate(self, chunks: List[Chunk]) -> List[Chunk]:
        pass
```

### Creating Custom Metadata Generators

```python
from klovis.base import BaseMetadataGenerator
from klovis.models import Chunk
from typing import List

class CustomMetadataGenerator(BaseMetadataGenerator):
    def generate(self, chunks: List[Chunk]) -> List[Chunk]:
        enriched = []
        for chunk in chunks:
            new_metadata = {
                **chunk.metadata,
                "custom_field": "value",
            }
            enriched.append(chunk.model_copy(update={"metadata": new_metadata}))
        return enriched
```

