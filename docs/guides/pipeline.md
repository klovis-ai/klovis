# Pipeline Guide

`KlovisPipeline` orchestrates the entire document processing workflow from loading to final output.

## Overview

`KlovisPipeline` provides a unified interface to execute multiple processing stages in sequence:

```
Loader → Extractor → Cleaner → Chunker → MetadataGenerator → Output
```

## Basic Usage

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

# Execute
documents = pipeline.loader.load()  # DirectoryLoader needs manual load
chunks = pipeline.run(documents)
```

## Parameters

- `loader` (BaseLoader, optional): Document loader
- `extractor` (BaseExtractor, optional): Content extractor
- `cleaner` (BaseCleaner, optional): Text cleaner
- `chunker` (BaseChunker, optional): Document chunker
- `metadata_generator` (BaseMetadataGenerator, optional): Metadata generator
- `require_api_key` (bool): Require API key validation (default: True)
- `export_results` (bool): Export results to file (default: False)
- `export_dir` (str): Export directory (default: "outputs")
- `export_format` (str): Export format - "json", "csv", or "parquet" (default: "json")

## Execution Flow

The pipeline executes stages in order:

1. **Loader**: Loads documents from sources
2. **Extractor**: Extracts content (if provided)
3. **Cleaner**: Cleans and normalizes text
4. **Chunker**: Splits into chunks
5. **Metadata Generator**: Enriches with metadata

## Export Formats

### JSON Export

```python
pipeline = KlovisPipeline(
    loader=loader,
    chunker=chunker,
    export_results=True,
    export_format="json",
)
```

### CSV Export

```python
pipeline = KlovisPipeline(
    loader=loader,
    chunker=chunker,
    export_results=True,
    export_format="csv",
)
```

### Parquet Export

```python
pipeline = KlovisPipeline(
    loader=loader,
    chunker=chunker,
    export_results=True,
    export_format="parquet",
)
```

## DirectoryLoader Special Case

`DirectoryLoader.load()` doesn't accept arguments, so handle it separately:

```python
# Create pipeline
pipeline = KlovisPipeline(
    loader=DirectoryLoader(path="data/"),
    cleaner=cleaner,
    chunker=chunker,
)

# Load manually, then run pipeline
documents = pipeline.loader.load()
chunks = pipeline.run(documents)
```

## Error Handling

The pipeline includes built-in error handling:

```python
try:
    chunks = pipeline.run(sources)
except ProcessingError as e:
    print(f"Pipeline failed: {e}")
except KlovisError as e:
    print(f"Klovis error: {e}")
```

## Logging

The pipeline logs each stage:

```
[INFO] === Starting KlovisPipeline Execution ===
[INFO] [1/5] Running loader...
[INFO] [2/5] Running extractor...
[INFO] [3/5] Running cleaner...
[INFO] [4/5] Running chunker...
[INFO] [5/5] Running metadata generator...
[INFO] Pipeline execution completed successfully.
[INFO] Total processing time: 2.34 seconds
```

## Complete Example

```python
from klovis.pipeline import KlovisPipeline
from klovis.loaders import DirectoryLoader
from klovis.cleaning import CompositeCleaner, HTMLCleaner, TextCleaner, NormalizeCleaner
from klovis.chunking import SimpleChunker
from klovis.metadata.metadata_generator import MetadataGenerator

# Configure all components
pipeline = KlovisPipeline(
    loader=DirectoryLoader(
        path="data/",
        recursive=True,
        markdownify=True,
    ),
    cleaner=CompositeCleaner([
        HTMLCleaner(),
        TextCleaner(),
        NormalizeCleaner(lowercase=True),
    ]),
    chunker=SimpleChunker(
        chunk_size=1000,
        chunk_overlap=100,
    ),
    metadata_generator=MetadataGenerator(),
    require_api_key=False,
    export_results=True,
    export_format="json",
)

# Execute
documents = pipeline.loader.load()
chunks = pipeline.run(documents)

print(f"✅ Processed {len(chunks)} chunks")
```

## Best Practices

1. **Use for complex workflows**: Pipeline simplifies multi-stage processing
2. **Enable export**: Use `export_results=True` for production
3. **Handle DirectoryLoader**: Load manually before running pipeline
4. **Monitor logs**: Check logs for performance and errors
5. **Test incrementally**: Test each stage before combining

## Next Steps

- See [API Reference](../api/pipeline.md) for complete API documentation
- Check [Examples](../examples/) for pipeline patterns
- Learn about [Custom Components](../advanced/custom-components.md)

