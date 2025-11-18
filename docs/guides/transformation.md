# Transformation Guide

Transformers convert processed chunks into different output formats for storage, indexing, or model ingestion.

## Overview

Klovis provides transformers to format chunks:

- **MarkdownTransformer**: Converts chunks to Markdown format

## MarkdownTransformer

Converts chunks into Markdown-formatted output.

### Basic Usage

```python
from klovis.transforming import MarkdownTransformer
from klovis.models import Chunk

chunks = [
    Chunk(
        text="Content here",
        metadata={"chunk_id": 0, "source": "doc.txt"}
    ),
]

transformer = MarkdownTransformer(include_metadata=True)
markdown_chunks = transformer.transform(chunks)

print(markdown_chunks[0]["markdown"])
```

### Parameters

- `include_metadata` (bool): Include metadata in Markdown output (default: True)

### Output Format

The transformer returns a list of dictionaries:

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

## Custom Transformers

Create custom transformers by inheriting from `BaseTransformer`:

```python
from klovis.base import BaseTransformer
from klovis.models import Chunk
from typing import List, Dict

class CustomTransformer(BaseTransformer):
    def transform(self, chunks: List[Chunk]) -> List[Dict]:
        results = []
        for chunk in chunks:
            # Your transformation logic
            results.append({
                "id": chunk.metadata.get("chunk_id"),
                "text": chunk.text,
                "custom_format": "...",
            })
        return results
```

## Use Cases

### Export to Markdown

```python
transformer = MarkdownTransformer(include_metadata=True)
markdown_output = transformer.transform(chunks)

# Save to file
with open("output.md", "w") as f:
    for item in markdown_output:
        f.write(item["markdown"])
```

### Format for Vector Database

```python
# Transform to format suitable for vector DB
transformer = MarkdownTransformer(include_metadata=False)
formatted = transformer.transform(chunks)

# Extract just the text for embedding
texts = [item["markdown"] for item in formatted]
```

## Best Practices

1. **Choose format**: Select format based on downstream use
2. **Include metadata**: Keep metadata when it's useful
3. **Consistent format**: Use consistent formatting across chunks
4. **Performance**: Transformers are fast; batch processing is efficient

## Next Steps

- See [API Reference](../api/transformers.md) for complete API documentation
- Check [Examples](../examples/) for transformation patterns
- Learn about [Pipeline](pipeline.md) for complete workflows

