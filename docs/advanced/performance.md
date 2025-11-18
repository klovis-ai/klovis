# Performance Optimization

Tips and best practices for optimizing Klovis pipeline performance.

## Batch Processing

Klovis components are designed for batch processing. Process multiple documents at once:

```python
# Good: Process all documents at once
documents = loader.load()
cleaned = cleaner.clean(documents)
chunks = chunker.chunk(cleaned)

# Avoid: Processing one at a time
for doc in documents:
    cleaned = cleaner.clean([doc])
    chunks = chunker.chunk(cleaned)
```

## Embedding Optimization

For `SemanticMerger`, optimize batch size:

```python
# Adjust batch_size based on your embedder
merger = SemanticMerger(
    embedder=embedder,
    batch_size=32,  # Larger batches = faster, but more memory
    max_size=2000,
)
```

**Guidelines:**
- **Small datasets** (< 100 chunks): `batch_size=10-20`
- **Medium datasets** (100-1000 chunks): `batch_size=32-64`
- **Large datasets** (> 1000 chunks): `batch_size=64-128`

## Memory Management

### Filter Early

Remove empty or invalid documents early:

```python
# Filter before processing
documents = [d for d in loader.load() if d.content.strip()]
cleaned = cleaner.clean(documents)
```

### Process in Batches

For very large datasets, process in batches:

```python
all_chunks = []
batch_size = 100

for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    cleaned = cleaner.clean(batch)
    chunks = chunker.chunk(cleaned)
    all_chunks.extend(chunks)
```

## Chunking Performance

### Choose Appropriate Chunk Size

Larger chunks = fewer chunks = faster processing:

```python
# For speed: larger chunks
chunker = SimpleChunker(chunk_size=2000, chunk_overlap=200)

# For quality: smaller chunks (slower)
chunker = SimpleChunker(chunk_size=500, chunk_overlap=50)
```

### Avoid Unnecessary Overlap

Reduce overlap if not needed:

```python
# Minimal overlap for speed
chunker = SimpleChunker(chunk_size=1000, chunk_overlap=50)
```

## Cleaning Performance

### Use Only Necessary Cleaners

Each cleaner adds processing time:

```python
# Minimal cleaning for speed
cleaner = TextCleaner()

# Full cleaning (slower)
cleaner = CompositeCleaner([
    HTMLCleaner(),
    TextCleaner(),
    NormalizeCleaner(),
    EmojiCleaner(),
])
```

### Skip Cleaning When Not Needed

If documents are already clean, skip cleaning:

```python
pipeline = KlovisPipeline(
    loader=loader,
    cleaner=None,  # Skip cleaning
    chunker=chunker,
)
```

## Caching

Cache expensive operations:

```python
import pickle

# Cache embeddings
if os.path.exists("embeddings.pkl"):
    with open("embeddings.pkl", "rb") as f:
        embeddings = pickle.load(f)
else:
    embeddings = embedder.embed(texts)
    with open("embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)
```

## Parallel Processing

For independent operations, use parallel processing:

```python
from concurrent.futures import ProcessPoolExecutor

def process_document(doc):
    cleaned = cleaner.clean([doc])
    chunks = chunker.chunk(cleaned)
    return chunks

with ProcessPoolExecutor() as executor:
    all_chunks = executor.map(process_document, documents)
```

## Profiling

Identify bottlenecks:

```python
import cProfile

profiler = cProfile.Profile()
profiler.enable()

# Your pipeline code
chunks = pipeline.run(sources)

profiler.disable()
profiler.print_stats()
```

## Best Practices

1. **Batch process**: Process multiple documents at once
2. **Filter early**: Remove invalid documents before processing
3. **Optimize batch sizes**: Adjust based on your data size
4. **Use appropriate chunk sizes**: Balance quality and speed
5. **Skip unnecessary steps**: Don't clean if already clean
6. **Cache expensive operations**: Save embeddings, etc.
7. **Profile your pipeline**: Identify bottlenecks

