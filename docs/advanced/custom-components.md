# Custom Components

Learn how to create custom loaders, cleaners, chunkers, and other components for Klovis.

## Overview

All Klovis components inherit from base classes, making it easy to create custom implementations that integrate seamlessly with the framework.

## Creating a Custom Loader

Inherit from `BaseLoader` and implement the `load()` method:

```python
from klovis.base import BaseLoader
from klovis.models import Document
from typing import List

class CustomLoader(BaseLoader):
    def load(self, sources: List[str]) -> List[Document]:
        documents = []
        for source in sources:
            # Your loading logic
            with open(source, 'r') as f:
                content = f.read()
            
            doc = Document(
                source=source,
                content=content,
                metadata={"loader": "custom"}
            )
            documents.append(doc)
        
        return documents
```

## Creating a Custom Cleaner

Inherit from `BaseCleaner` and implement the `clean()` method:

```python
from klovis.base import BaseCleaner
from klovis.models import Document
from typing import List
import re

class CustomCleaner(BaseCleaner):
    def clean(self, documents: List[Document]) -> List[Document]:
        cleaned = []
        for doc in documents:
            # Your cleaning logic
            cleaned_content = re.sub(r'\s+', ' ', doc.content)
            
            cleaned_doc = Document(
                source=doc.source,
                content=cleaned_content,
                metadata=doc.metadata  # Preserve metadata
            )
            cleaned.append(cleaned_doc)
        
        return cleaned
```

## Creating a Custom Chunker

Inherit from `BaseChunker` and implement the `chunk()` method:

```python
from klovis.base import BaseChunker
from klovis.models import Document, Chunk
from typing import List

class CustomChunker(BaseChunker):
    def __init__(self, sentences_per_chunk: int = 5):
        self.sentences_per_chunk = sentences_per_chunk
    
    def chunk(self, documents: List[Document]) -> List[Chunk]:
        chunks = []
        for doc in documents:
            sentences = doc.content.split('. ')
            
            for i in range(0, len(sentences), self.sentences_per_chunk):
                chunk_text = '. '.join(sentences[i:i+self.sentences_per_chunk])
                
                chunk = Chunk(
                    text=chunk_text,
                    metadata={
                        "chunk_id": len(chunks),
                        "source": doc.source,
                        "type": "sentence-based"
                    }
                )
                chunks.append(chunk)
        
        return chunks
```

## Creating a Custom Merger

Inherit from `BaseMerger` and implement the `merge()` method:

```python
from klovis.base import BaseMerger
from klovis.models import Chunk
from typing import List

class CustomMerger(BaseMerger):
    def __init__(self, max_size: int = 2000):
        self.max_size = max_size
    
    def merge(self, chunks: List[Chunk]) -> List[Chunk]:
        merged = []
        current_chunk = None
        
        for chunk in chunks:
            if current_chunk is None:
                current_chunk = chunk
            elif len(current_chunk.text) + len(chunk.text) <= self.max_size:
                # Merge chunks
                current_chunk = Chunk(
                    text=current_chunk.text + "\n\n" + chunk.text,
                    metadata={
                        **current_chunk.metadata,
                        "merged": True
                    }
                )
            else:
                # Start new chunk
                merged.append(current_chunk)
                current_chunk = chunk
        
        if current_chunk:
            merged.append(current_chunk)
        
        return merged
```

## Creating a Custom Transformer

Inherit from `BaseTransformer` and implement the `transform()` method:

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
                "source": chunk.metadata.get("source"),
                "custom_format": f"[{chunk.metadata.get('source')}] {chunk.text}"
            })
        return results
```

## Best Practices

1. **Preserve Metadata**: Always preserve existing metadata when creating new objects
2. **Handle Errors**: Implement proper error handling
3. **Log Operations**: Use `get_logger()` for logging
4. **Type Hints**: Use proper type hints for better IDE support
5. **Documentation**: Add docstrings explaining your component's behavior

## Integration

Custom components work seamlessly with KlovisPipeline:

```python
from klovis.pipeline import KlovisPipeline

pipeline = KlovisPipeline(
    loader=CustomLoader(),
    cleaner=CustomCleaner(),
    chunker=CustomChunker(),
)

results = pipeline.run(sources)
```

## Testing Custom Components

Test your custom components:

```python
def test_custom_loader():
    loader = CustomLoader()
    docs = loader.load(["test.txt"])
    assert len(docs) > 0
    assert all(isinstance(d, Document) for d in docs)
```

## Next Steps

- See [API Reference](../api/) for base class details
- Check [Examples](../examples/) for more patterns
- Review existing components for implementation patterns

