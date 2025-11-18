# Configuration Reference

Configuration options and environment variables for Klovis.

## Environment Variables

Klovis uses environment variables for configuration.

### KLOVIS_API_KEY

API key for Klovis services (if required).

```bash
export KLOVIS_API_KEY="your-api-key-here"
```

Or in Python:
```python
import os
os.environ["KLOVIS_API_KEY"] = "your-api-key-here"
```

### LOG_LEVEL

Logging level for Klovis components.

**Values:**
- `DEBUG`: Detailed debugging information
- `INFO`: General informational messages (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages only
- `CRITICAL`: Critical errors only

```bash
export LOG_LEVEL="DEBUG"
```

## Settings

Access configuration through the `settings` object:

```python
from klovis.config import settings

# Check if API key is set
if settings.has_api_key():
    print("API key is configured")

# Require API key (raises MissingAPIKeyError if not set)
settings.require_api_key()

# Get log level
print(settings.LOG_LEVEL)
```

## Logger Configuration

Klovis uses a centralized logging system:

```python
from klovis.utils import get_logger

logger = get_logger(__name__)
logger.info("Message")
logger.debug("Debug message")
logger.warning("Warning message")
logger.error("Error message")
```

The logger automatically:
- Formats messages with timestamps
- Includes module names
- Respects LOG_LEVEL environment variable
- Outputs to stdout

## Component-Specific Configuration

### Loaders

Loaders are configured during initialization:

```python
loader = DirectoryLoader(
    path="data/",
    recursive=True,
    ignore_hidden=True,
    markdownify=True,
)
```

### Cleaners

Cleaners accept configuration parameters:

```python
cleaner = NormalizeCleaner(
    lowercase=True,
    preserve_newlines=True,
)
```

### Chunkers

Chunkers are configured with size and overlap:

```python
chunker = SimpleChunker(
    chunk_size=1000,
    chunk_overlap=100,
    smart_overlap=True,
)
```

### Mergers

Mergers require an embedder and clustering parameters:

```python
merger = SemanticMerger(
    embedder=embedder,
    max_size=2000,
    batch_size=32,
    distance_threshold=0.3,
)
```

## Best Practices

1. **Use environment variables** for sensitive configuration
2. **Set LOG_LEVEL** appropriately for your environment
3. **Validate configuration** before running pipelines
4. **Document custom settings** in your project

