# Mergers API Reference

Complete API documentation for merger classes.

## SemanticMerger

Groups chunks by semantic similarity using embeddings and hierarchical clustering.

### Class Definition

```python
class SemanticMerger(BaseMerger):
    def __init__(
        self,
        embedder,
        max_size: int = 2000,
        batch_size: int = 10,
        n_clusters: int | None = None,
        distance_threshold: float | None = 0.1,
    )
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `embedder` | `BaseEmbedder` | Required | Embedder instance for generating embeddings |
| `max_size` | `int` | `2000` | Maximum characters per merged chunk |
| `batch_size` | `int` | `10` | Number of chunks to embed at once |
| `n_clusters` | `int \| None` | `None` | Fixed number of clusters (if None, uses distance_threshold) |
| `distance_threshold` | `float \| None` | `0.1` | Maximum distance for clustering (cosine distance) |

### Methods

#### `merge(chunks: List[Chunk]) -> List[Chunk]`

Merges chunks based on semantic similarity.

**Parameters:**
- `chunks` (`List[Chunk]`): Chunks to merge

**Returns:**
- `List[Chunk]`: List of merged chunks

**Example:**
```python
merger = SemanticMerger(
    embedder=embedder,
    max_size=2000,
    distance_threshold=0.3,
)
merged = merger.merge(chunks)
```

### How It Works

1. **Embedding**: Converts all chunks to embeddings using the provided embedder
2. **Clustering**: Groups similar chunks using hierarchical clustering with `complete` linkage
3. **Sorting**: Sorts chunks within each cluster by similarity to cluster centroid
4. **Merging**: Combines chunks up to `max_size` limit

### Distance Threshold

For cosine distance:
- `0.0` = identical (similarity = 1.0)
- `1.0` = orthogonal (similarity = 0.0)
- `2.0` = opposite (similarity = -1.0)

**Recommended values:**
- `0.2-0.3`: Tight clusters, high similarity required
- `0.3-0.5`: Moderate clustering
- `0.5+`: Loose clusters, more diverse chunks

### Error Handling

The merger handles embedding errors gracefully:
- Failed embeddings are skipped
- Processing continues with successfully embedded chunks
- Warnings are logged for failed batches

### Merged Chunk Metadata

Merged chunks include detailed metadata:

```python
{
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

---

## BaseMerger

Abstract base class for all mergers.

### Class Definition

```python
class BaseMerger(ABC):
    @abstractmethod
    def merge(self, chunks: List[Chunk]) -> List[Chunk]:
        pass
```

### Creating Custom Mergers

```python
from klovis.base import BaseMerger
from klovis.models import Chunk
from typing import List

class CustomMerger(BaseMerger):
    def merge(self, chunks: List[Chunk]) -> List[Chunk]:
        # Your merging logic
        merged = []
        # ...
        return merged
```

