# Merging Guide

Merging combines semantically similar chunks to create larger, more coherent pieces while respecting size constraints.

## Overview

Klovis provides `SemanticMerger` which uses embeddings and clustering to merge similar chunks.

## SemanticMerger

Groups chunks by semantic similarity using embeddings and hierarchical clustering.

### Basic Usage

```python
from klovis.merger import SemanticMerger
from your_embedder import YourEmbedder

# Create embedder (you need to provide this)
embedder = YourEmbedder()

# Create merger
merger = SemanticMerger(
    embedder=embedder,
    max_size=2000,  # Maximum characters per merged chunk
    batch_size=32,  # Batch size for embedding
    distance_threshold=0.3,  # Clustering threshold
)

# Merge chunks
merged_chunks = merger.merge(chunks)
```

### Parameters

- `embedder`: Embedder instance (must implement `embed()` method)
- `max_size` (int): Maximum characters per merged chunk (default: 2000)
- `batch_size` (int): Number of chunks to embed at once (default: 10)
- `n_clusters` (int, optional): Fixed number of clusters (default: None)
- `distance_threshold` (float, optional): Maximum distance for clustering (default: 0.1)

### How It Works

1. **Embedding**: Converts all chunks to embeddings using the provided embedder
2. **Clustering**: Groups similar chunks using hierarchical clustering
3. **Sorting**: Sorts chunks within each cluster by similarity to cluster centroid
4. **Merging**: Combines chunks up to `max_size` limit

### Distance Threshold

The `distance_threshold` parameter controls cluster size:
- **Lower values** (0.1-0.3): Tighter clusters, more similar chunks
- **Higher values** (0.5-1.0): Looser clusters, more diverse chunks

For cosine distance:
- `0.0` = identical (similarity = 1.0)
- `1.0` = orthogonal (similarity = 0.0)
- `2.0` = opposite (similarity = -1.0)

**Recommended**: Start with `0.3` and adjust based on your data.

### Linkage Methods

The merger uses `complete` linkage by default, which ensures all chunks in a cluster are similar to each other (not just to the centroid).

## Metadata

Merged chunks include detailed metadata:

```python
chunk.metadata = {
    "chunk_id": 0,
    "type": "semantic",
    "cluster_id": 1,
    "n_cluster_chunks": 5,  # Total chunks in cluster
    "cluster_chunk_index": 0,  # Index within cluster
    "n_merged_chunks": 3,  # Chunks merged into this chunk
    "merged_chunks_details": [
        {"chunk_id": 5, "similarity": 0.95},
        {"chunk_id": 2, "similarity": 0.92},
        {"chunk_id": 8, "similarity": 0.89},
    ],
    "similarity_scores": [0.95, 0.92, 0.89],
    "cluster_all_chunks_details": [...],  # All chunks in cluster
    "cluster_all_similarity_scores": [...],  # All scores in cluster
}
```

## Error Handling

The merger handles embedding errors gracefully:

```python
# If embedding fails for some chunks, they're skipped
# The merger continues with successfully embedded chunks
merged = merger.merge(chunks)
```

## Example: Complete Workflow

```python
from klovis.chunking import SimpleChunker
from klovis.merger import SemanticMerger
from your_embedder import YourEmbedder

# 1. Create initial chunks
chunker = SimpleChunker(chunk_size=500, chunk_overlap=50)
chunks = chunker.chunk(documents)

# 2. Merge semantically similar chunks
embedder = YourEmbedder()
merger = SemanticMerger(
    embedder=embedder,
    max_size=2000,
    distance_threshold=0.3,
)

merged = merger.merge(chunks)

print(f"Reduced {len(chunks)} chunks to {len(merged)} merged chunks")
```

## Best Practices

1. **Choose appropriate threshold**: Test different `distance_threshold` values
2. **Monitor cluster sizes**: Check if clusters are too large or too small
3. **Handle errors**: Embedding can fail; ensure error handling
4. **Batch size**: Adjust `batch_size` based on embedder capabilities
5. **Max size**: Set `max_size` based on your downstream requirements

## Performance Considerations

- **Batch size**: Larger batches are faster but use more memory
- **Embedding time**: Embedding is usually the bottleneck
- **Clustering**: Scales well for hundreds to thousands of chunks
- **Memory**: Store embeddings efficiently for large datasets

## Troubleshooting

### Too Many Small Clusters

**Problem**: Many single-chunk clusters

**Solution**: Increase `distance_threshold`:
```python
merger = SemanticMerger(embedder=embedder, distance_threshold=0.5)
```

### Too Few Large Clusters

**Problem**: Everything grouped into one cluster

**Solution**: Decrease `distance_threshold`:
```python
merger = SemanticMerger(embedder=embedder, distance_threshold=0.2)
```

### Embedding Errors

**Problem**: Some chunks fail to embed

**Solution**: The merger handles this automatically, but check embedder configuration

## Next Steps

- Learn about [Metadata](metadata.md) to enrich merged chunks
- See [API Reference](../api/mergers.md) for complete API documentation
- Check [Examples](../examples/) for merging patterns

