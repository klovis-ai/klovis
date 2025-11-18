# Utilities Reference

Utility functions and helpers provided by Klovis.

## Logger

### `get_logger(name: str) -> logging.Logger`

Creates and returns a configured logger instance.

**Parameters:**
- `name` (`str`): Logger name (typically `__name__`)

**Returns:**
- `logging.Logger`: Configured logger instance

**Example:**
```python
from klovis.utils import get_logger

logger = get_logger(__name__)
logger.info("Processing started")
logger.debug("Debug information")
logger.error("An error occurred")
```

**Features:**
- Automatic formatting with timestamps
- Module name inclusion
- Respects `LOG_LEVEL` environment variable
- Outputs to stdout

**Log Format:**
```
[2024-01-01 12:00:00] [INFO] [module_name] Message
```

## Models Utilities

### Document and Chunk Serialization

Both `Document` and `Chunk` models provide serialization methods:

#### `to_dict() -> Dict[str, Any]`

Converts model to dictionary.

```python
doc = Document(source="test.txt", content="Content")
doc_dict = doc.to_dict()
# {"source": "test.txt", "content": "Content", "metadata": {}}
```

#### `to_json(indent: int = 2) -> str`

Converts model to JSON string.

```python
doc = Document(source="test.txt", content="Content")
json_str = doc.to_json(indent=4)
```

## Configuration Utilities

### Settings Access

```python
from klovis.config import settings

# Check API key
if settings.has_api_key():
    print("API key is set")

# Require API key
settings.require_api_key()  # Raises MissingAPIKeyError if not set

# Access log level
print(settings.LOG_LEVEL)
```

## Best Practices

1. **Use get_logger()** for consistent logging across modules
2. **Serialize models** when storing or transmitting data
3. **Check settings** before operations requiring configuration
4. **Handle errors** gracefully with proper logging

