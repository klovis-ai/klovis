# Core Concepts

Understanding Klovis's architecture and design principles will help you use it effectively.

## Architecture Overview

Klovis follows a modular, pipeline-based architecture where documents flow through a series of processing stages:

```
Documents → Loaders → Cleaners → Chunkers → Mergers → Transformers → Output
```

Each stage is independent and can be used standalone or combined in a pipeline.

## Key Concepts

### Documents and Chunks

**Document**: Represents a raw or loaded document with:
- `source`: Path, URL, or identifier
- `content`: Text content
- `metadata`: Additional information (dict)

**Chunk**: Represents a processed piece of text with:
- `text`: Chunk content
- `metadata`: Processing information (chunk_id, source, etc.)

### Processing Stages

#### 1. Loading
Convert files, URLs, or data into `Document` objects.

**Example:**
```python
from klovis.loaders import DirectoryLoader

loader = DirectoryLoader(path="data/")
documents = loader.load()  # Returns List[Document]
```

#### 2. Cleaning
Normalize and clean document text.

**Example:**
```python
from klovis.cleaning import HTMLCleaner, TextCleaner

cleaner = HTMLCleaner()
cleaned = cleaner.clean(documents)  # Returns List[Document]
```

#### 3. Chunking
Split documents into smaller, manageable pieces.

**Example:**
```python
from klovis.chunking import SimpleChunker

chunker = SimpleChunker(chunk_size=1000)
chunks = chunker.chunk(documents)  # Returns List[Chunk]
```

#### 4. Merging (Optional)
Combine semantically similar chunks.

**Example:**
```python
from klovis.merger import SemanticMerger

merger = SemanticMerger(embedder=embedder, max_size=2000)
merged = merger.merge(chunks)  # Returns List[Chunk]
```

#### 5. Transformation (Optional)
Convert chunks to different output formats.

**Example:**
```python
from klovis.transforming import MarkdownTransformer

transformer = MarkdownTransformer()
output = transformer.transform(chunks)  # Returns List[Dict]
```

## Design Principles

### 1. Modularity
Each component is independent and can be used separately or combined.

### 2. Extensibility
All components inherit from base classes, making it easy to create custom implementations.

### 3. Type Safety
Uses Pydantic models for type validation and serialization.

### 4. Composability
Components can be chained together to create complex pipelines.

### 5. Metadata Preservation
Metadata flows through the pipeline and can be enriched at each stage.

## Data Flow

```
┌─────────────┐
│   Sources   │  (files, URLs, data)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Loaders   │  → List[Document]
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Cleaners   │  → List[Document] (cleaned)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Chunkers   │  → List[Chunk]
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Mergers   │  → List[Chunk] (merged) [Optional]
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Transformers │  → List[Dict] [Optional]
└─────────────┘
```

## Base Classes

All Klovis components inherit from base classes:

- `BaseLoader`: Abstract base for loaders
- `BaseCleaner`: Abstract base for cleaners
- `BaseChunker`: Abstract base for chunkers
- `BaseMerger`: Abstract base for mergers
- `BaseTransformer`: Abstract base for transformers
- `BaseMetadataGenerator`: Abstract base for metadata generators

This allows you to create custom components that integrate seamlessly with Klovis.

## Best Practices

1. **Start Simple**: Begin with basic components and add complexity as needed
2. **Preserve Metadata**: Use metadata to track document provenance
3. **Handle Errors**: Implement error handling for production use
4. **Test Components**: Test each stage independently before combining
5. **Use Pipelines**: Use `KlovisPipeline` for complex workflows

## Next Steps

- Learn about specific components in the [User Guides](guides/)
- See [Custom Components](advanced/custom-components.md) for extending Klovis
- Check [Examples](examples/) for real-world usage patterns

