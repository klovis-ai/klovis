# Building a RAG Pipeline with Klovis

This tutorial shows how to build a complete RAG (Retrieval-Augmented Generation) pipeline using Klovis.

## Overview

A typical RAG pipeline involves:
1. **Document Ingestion** (Klovis)
2. **Embedding** (Vector DB)
3. **Storage** (Vector Database)
4. **Retrieval** (Similarity Search)
5. **Generation** (LLM)

Klovis handles step 1 - preparing documents for embedding and storage.

## Step 1: Document Processing with Klovis

```python
from klovis.loaders import DirectoryLoader
from klovis.cleaning import CompositeCleaner, HTMLCleaner, TextCleaner
from klovis.chunking import SimpleChunker
from klovis.merger import SemanticMerger
from your_embedder import YourEmbedder

# 1. Load documents
loader = DirectoryLoader(path="documents/", recursive=True, markdownify=True)
documents = loader.load()

# 2. Clean documents
cleaner = CompositeCleaner([
    HTMLCleaner(),
    TextCleaner(),
    NormalizeCleaner(lowercase=True),
])
cleaned = cleaner.clean(documents)

# 3. Chunk documents
chunker = SimpleChunker(chunk_size=1000, chunk_overlap=100)
chunks = chunker.chunk(cleaned)

# 4. Merge similar chunks (optional)
embedder = YourEmbedder()
merger = SemanticMerger(embedder=embedder, max_size=2000, distance_threshold=0.3)
merged_chunks = merger.merge(chunks)

print(f"Ready for embedding: {len(merged_chunks)} chunks")
```

## Step 2: Embedding and Storage

```python
# Embed chunks
embeddings = embedder.embed([chunk.text for chunk in merged_chunks])

# Store in vector database (example with FAISS)
import faiss
import numpy as np

# Create index
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)

# Add embeddings
index.add(np.array(embeddings))

# Store chunks metadata
chunk_metadata = [chunk.to_dict() for chunk in merged_chunks]
```

## Step 3: Retrieval

```python
# Query embedding
query = "What is the main topic?"
query_embedding = embedder.embed([query])[0]

# Search
k = 5  # Number of results
distances, indices = index.search(np.array([query_embedding]), k)

# Retrieve chunks
results = [merged_chunks[i] for i in indices[0]]
```

## Step 4: Generation

```python
# Build context from retrieved chunks
context = "\n\n".join([chunk.text for chunk in results])

# Generate with LLM
prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
response = llm.generate(prompt)
```

## Complete Example

```python
from klovis.pipeline import KlovisPipeline
from klovis.loaders import DirectoryLoader
from klovis.cleaning import CompositeCleaner, HTMLCleaner, TextCleaner
from klovis.chunking import SimpleChunker
from klovis.merger import SemanticMerger

# Setup Klovis pipeline
pipeline = KlovisPipeline(
    loader=DirectoryLoader(path="documents/", recursive=True),
    cleaner=CompositeCleaner([HTMLCleaner(), TextCleaner()]),
    chunker=SimpleChunker(chunk_size=1000),
    require_api_key=False,
)

# Process documents
documents = pipeline.loader.load()
chunks = pipeline.run(documents)

# Ready for RAG pipeline
# chunks are now ready for embedding and storage
```

## Best Practices

1. **Chunk Size**: Use 500-1000 characters for better embedding quality
2. **Overlap**: 10-20% overlap preserves context
3. **Cleaning**: Clean thoroughly before chunking
4. **Metadata**: Preserve metadata for filtering and retrieval
5. **Semantic Merging**: Use for better chunk coherence

## Next Steps

- Integrate with your vector database
- Set up embedding pipeline
- Implement retrieval logic
- Connect to your LLM

