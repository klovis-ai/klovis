# Metadata Guide

Metadata provides additional information about documents and chunks, enabling better organization and retrieval.

## Overview

Klovis includes metadata generation capabilities to enrich chunks with useful information:

- **MetadataGenerator**: Basic metadata generation (length, tags)
- **EnrichedChunksGenerator**: Advanced LLM-based enrichment (FAQ, summary, topics, etc.)

## MetadataGenerator

Generates basic metadata for chunks.

### Basic Usage

```python
from klovis.metadata.metadata_generator import MetadataGenerator
from klovis.models import Chunk

chunks = [
    Chunk(text="Content here", metadata={"chunk_id": 0}),
]

generator = MetadataGenerator()
enriched = generator.generate(chunks)

# Enriched chunks now have additional metadata
print(enriched[0].metadata)
# {
#     "chunk_id": 0,
#     "length": 13,
#     "tags": ["example"]
# }
```

### Generated Metadata

- `length`: Character count of the chunk text
- `tags`: List of tags (default: `["example"]`)

### Preserving Existing Metadata

The generator preserves existing metadata:

```python
chunk = Chunk(
    text="Content",
    metadata={"chunk_id": 0, "source": "doc.txt", "custom": "value"}
)

generator = MetadataGenerator()
enriched = generator.generate([chunk])[0]

# All metadata is preserved
assert enriched.metadata["chunk_id"] == 0
assert enriched.metadata["source"] == "doc.txt"
assert enriched.metadata["custom"] == "value"
assert "length" in enriched.metadata  # New metadata added
```

## EnrichedChunksGenerator

Generates rich metadata using LLM capabilities (FAQ, summaries, topics, etc.).

### Basic Usage

```python
from klovis.metadata import EnrichedChunksGenerator
from your_llm_client import YourLLMClient

llm_client = YourLLMClient()

generator = EnrichedChunksGenerator(
    llm_client=llm_client,
    enabled=["faq", "summary", "topics"],
    summary_sentences=5,
    topics_count=10,
)

enriched = generator.generate(chunks)
```

### Available Features

- `faq`: Generate FAQ pairs
- `summary`: Generate text summaries
- `topics`: Extract main topics
- `title`: Generate titles
- `keywords`: Extract keywords
- `numerical_insights`: Extract numerical data

### Parameters

- `llm_client`: LLM client instance
- `enabled` (List[str]): List of features to enable
- `summary_sentences` (int): Number of sentences in summary
- `topics_count` (int): Number of topics to extract
- `faq_count` (int): Number of FAQ pairs
- `keywords_count` (int): Number of keywords
- `numerical_items` (int): Number of numerical insights
- `max_output_chars` (int): Maximum output characters

## Metadata Structure

### Basic Metadata

```python
{
    "chunk_id": 0,
    "source": "doc.txt",
    "length": 500,
    "tags": ["example"]
}
```

### Enriched Metadata

```python
{
    "chunk_id": 0,
    "source": "doc.txt",
    "length": 500,
    "faq": [...],
    "summary": "...",
    "topics": [...],
    "title": "...",
    "keywords": [...],
    "numerical_insights": [...]
}
```

## Best Practices

1. **Preserve metadata**: Don't overwrite important metadata
2. **Use selectively**: Only generate needed metadata (LLM calls are expensive)
3. **Cache results**: Cache metadata generation for production
4. **Validate output**: Check metadata quality and format
5. **Handle errors**: LLM calls can fail; implement error handling

## Custom Metadata Generators

Create custom generators by inheriting from `BaseMetadataGenerator`:

```python
from klovis.base import BaseMetadataGenerator
from klovis.models import Chunk
from typing import List

class CustomMetadataGenerator(BaseMetadataGenerator):
    def generate(self, chunks: List[Chunk]) -> List[Chunk]:
        enriched = []
        for chunk in chunks:
            # Your metadata generation logic
            new_metadata = {
                **chunk.metadata,
                "custom_field": "value",
            }
            enriched.append(chunk.model_copy(update={"metadata": new_metadata}))
        return enriched
```

## Next Steps

- Learn about [Transformation](transformation.md) to format output
- See [API Reference](../api/metadata.md) for complete API documentation
- Check [Examples](../examples/) for metadata patterns

