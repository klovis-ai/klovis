# Quick Start Guide

Get started with Klovis in 5 minutes. This guide will walk you through a complete document processing pipeline.

## Your First Pipeline

Let's process a document from start to finish:

```python
from klovis.loaders import DirectoryLoader
from klovis.cleaning import HTMLCleaner, TextCleaner, CompositeCleaner
from klovis.chunking import SimpleChunker
from klovis.models import Document

# 1. Load documents
loader = DirectoryLoader(path="data/", recursive=True)
documents = loader.load()

# 2. Clean documents
cleaner = CompositeCleaner([
    HTMLCleaner(),
    TextCleaner(),
])
cleaned_docs = cleaner.clean(documents)

# 3. Chunk documents
chunker = SimpleChunker(chunk_size=1000, chunk_overlap=100)
chunks = chunker.chunk(cleaned_docs)

print(f"✅ Processed {len(documents)} documents into {len(chunks)} chunks")
```

## Using the Pipeline

For a more streamlined approach, use `KlovisPipeline`:

```python
from klovis.pipeline import KlovisPipeline
from klovis.loaders import DirectoryLoader
from klovis.cleaning import CompositeCleaner, HTMLCleaner, TextCleaner
from klovis.chunking import SimpleChunker

# Configure pipeline
pipeline = KlovisPipeline(
    loader=DirectoryLoader(path="data/", recursive=True),
    cleaner=CompositeCleaner([HTMLCleaner(), TextCleaner()]),
    chunker=SimpleChunker(chunk_size=1000),
    require_api_key=False,
)

# Execute (DirectoryLoader needs manual load)
documents = pipeline.loader.load()
chunks = pipeline.run(documents)

print(f"✅ Generated {len(chunks)} chunks")
```

## Processing a Single Document

```python
from klovis.models import Document
from klovis.cleaning import TextCleaner
from klovis.chunking import SimpleChunker

# Create a document
doc = Document(
    source="example.txt",
    content="Your document content here..."
)

# Clean it
cleaner = TextCleaner()
cleaned = cleaner.clean([doc])[0]

# Chunk it
chunker = SimpleChunker(chunk_size=500)
chunks = chunker.chunk([cleaned])

print(f"Created {len(chunks)} chunks")
```

## What's Next?

- Learn about [Core Concepts](concepts.md) to understand how Klovis works
- Explore [Loaders Guide](guides/loaders.md) for different document sources
- Check out [Advanced Examples](examples/advanced-examples.md) for complex use cases

