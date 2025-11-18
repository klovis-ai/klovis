# Error Handling

Best practices for handling errors in Klovis pipelines.

## Exception Types

Klovis defines several exception types:

```python
from klovis.exceptions import (
    KlovisError,
    MissingAPIKeyError,
    InvalidDataError,
    ProcessingError,
    ModuleDependencyError,
)
```

## Handling Loader Errors

### File Not Found

```python
from klovis.loaders import DirectoryLoader
from klovis.exceptions import KlovisError

try:
    loader = DirectoryLoader(path="data/")
    documents = loader.load()
except FileNotFoundError as e:
    print(f"Directory not found: {e}")
    # Handle error
except KlovisError as e:
    print(f"Klovis error: {e}")
```

### Invalid File Format

```python
try:
    loader = PDFLoader(path="document.pdf")
    documents = loader.load()
except Exception as e:
    print(f"Failed to load PDF: {e}")
    # Handle error or skip file
```

## Handling Cleaner Errors

Cleaners typically don't raise exceptions, but handle edge cases:

```python
from klovis.cleaning import HTMLCleaner

# Empty documents are handled gracefully
doc = Document(source="empty.html", content="")
cleaner = HTMLCleaner()
cleaned = cleaner.clean([doc])  # Returns empty document
```

## Handling Chunker Errors

### Empty Documents

```python
# Filter empty documents before chunking
documents = [d for d in documents if d.content.strip()]
chunks = chunker.chunk(documents)
```

### Very Large Documents

```python
try:
    chunks = chunker.chunk(documents)
except MemoryError:
    # Process in smaller batches
    all_chunks = []
    for doc in documents:
        chunks = chunker.chunk([doc])
        all_chunks.extend(chunks)
```

## Handling Merger Errors

### Embedding Failures

`SemanticMerger` handles embedding errors gracefully:

```python
from klovis.merger import SemanticMerger

# Failed embeddings are skipped automatically
merger = SemanticMerger(embedder=embedder, max_size=2000)
merged = merger.merge(chunks)  # Continues even if some embeddings fail
```

### Check for Empty Results

```python
merged = merger.merge(chunks)
if not merged:
    print("Warning: No chunks were merged")
    # Use original chunks as fallback
    merged = chunks
```

## Pipeline Error Handling

### Complete Error Handling

```python
from klovis.pipeline import KlovisPipeline
from klovis.exceptions import KlovisError, ProcessingError

try:
    pipeline = KlovisPipeline(
        loader=loader,
        cleaner=cleaner,
        chunker=chunker,
    )
    documents = pipeline.loader.load()
    chunks = pipeline.run(documents)
    
except ProcessingError as e:
    logger.error(f"Pipeline processing failed: {e}")
    # Handle processing error
    
except KlovisError as e:
    logger.error(f"Klovis error: {e}")
    # Handle general Klovis error
    
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Handle unexpected errors
```

## Graceful Degradation

### Continue on Partial Failure

```python
def process_with_fallback(documents):
    try:
        cleaned = cleaner.clean(documents)
        chunks = chunker.chunk(cleaned)
        return chunks
    except Exception as e:
        logger.warning(f"Processing failed: {e}, using original documents")
        # Fallback to original documents
        return [Chunk(text=d.content, metadata={"source": d.source}) 
                for d in documents]
```

### Skip Invalid Documents

```python
def process_safely(documents):
    valid_docs = []
    for doc in documents:
        try:
            # Validate document
            if not doc.content.strip():
                continue
            valid_docs.append(doc)
        except Exception as e:
            logger.warning(f"Skipping invalid document {doc.source}: {e}")
            continue
    
    return cleaner.clean(valid_docs)
```

## Logging Errors

Use Klovis logging for error tracking:

```python
from klovis.utils import get_logger

logger = get_logger(__name__)

try:
    chunks = pipeline.run(sources)
except Exception as e:
    logger.error(f"Pipeline failed: {e}", exc_info=True)
    # exc_info=True includes stack trace
```

## Best Practices

1. **Catch specific exceptions**: Handle each exception type appropriately
2. **Log errors**: Use logging to track errors in production
3. **Graceful degradation**: Continue processing when possible
4. **Validate input**: Check data before processing
5. **Handle edge cases**: Empty documents, very large files, etc.
6. **Provide context**: Include helpful error messages
7. **Test error paths**: Ensure error handling works correctly

