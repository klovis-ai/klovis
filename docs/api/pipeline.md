# Pipeline API Reference

Complete API documentation for KlovisPipeline.

## KlovisPipeline

Orchestrates the entire document processing workflow.

### Class Definition

```python
class KlovisPipeline:
    def __init__(
        self,
        loader: BaseLoader | None = None,
        extractor: BaseExtractor | None = None,
        cleaner: BaseCleaner | None = None,
        chunker: BaseChunker | None = None,
        metadata_generator: BaseMetadataGenerator | None = None,
        require_api_key: bool = True,
        export_results: bool = False,
        export_dir: str = "outputs",
        export_format: str = "json",
    )
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `loader` | `BaseLoader \| None` | `None` | Document loader |
| `extractor` | `BaseExtractor \| None` | `None` | Content extractor |
| `cleaner` | `BaseCleaner \| None` | `None` | Text cleaner |
| `chunker` | `BaseChunker \| None` | `None` | Document chunker |
| `metadata_generator` | `BaseMetadataGenerator \| None` | `None` | Metadata generator |
| `require_api_key` | `bool` | `True` | Require API key validation |
| `export_results` | `bool` | `False` | Export results to file |
| `export_dir` | `str` | `"outputs"` | Export directory |
| `export_format` | `str` | `"json"` | Export format: "json", "csv", or "parquet" |

### Methods

#### `run(sources: List[Any]) -> List[Chunk]`

Executes the pipeline sequentially.

**Parameters:**
- `sources` (`List[Any]`): Input sources (paths, URLs, or documents)

**Returns:**
- `List[Chunk]`: Processed chunks

**Execution Flow:**
1. Loader (if provided)
2. Extractor (if provided)
3. Cleaner (if provided)
4. Chunker (if provided)
5. Metadata Generator (if provided)

**Example:**
```python
from klovis.pipeline import KlovisPipeline
from klovis.loaders import DirectoryLoader
from klovis.cleaning import CompositeCleaner, HTMLCleaner
from klovis.chunking import SimpleChunker

pipeline = KlovisPipeline(
    loader=DirectoryLoader(path="data/"),
    cleaner=CompositeCleaner([HTMLCleaner()]),
    chunker=SimpleChunker(chunk_size=1000),
    require_api_key=False,
)

# DirectoryLoader needs manual load
documents = pipeline.loader.load()
chunks = pipeline.run(documents)
```

### Export Formats

#### JSON Export

```python
pipeline = KlovisPipeline(
    loader=loader,
    chunker=chunker,
    export_results=True,
    export_format="json",
)
```

#### CSV Export

```python
pipeline = KlovisPipeline(
    loader=loader,
    chunker=chunker,
    export_results=True,
    export_format="csv",
)
```

#### Parquet Export

```python
pipeline = KlovisPipeline(
    loader=loader,
    chunker=chunker,
    export_results=True,
    export_format="parquet",
)
```

### Logging

The pipeline logs each stage:

```
[INFO] === Starting KlovisPipeline Execution ===
[INFO] [1/5] Running loader...
[INFO] [2/5] Running extractor...
[INFO] [3/5] Running cleaner...
[INFO] [4/5] Running chunker...
[INFO] [5/5] Running metadata generator...
[INFO] Pipeline execution completed successfully.
```

### Error Handling

The pipeline includes built-in error handling and will raise appropriate exceptions if processing fails.

