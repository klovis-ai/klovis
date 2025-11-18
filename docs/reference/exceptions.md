# Exceptions Reference

Complete reference for all Klovis exceptions.

## Exception Hierarchy

```
KlovisError (base)
├── MissingAPIKeyError
├── InvalidDataError
├── ProcessingError
└── ModuleDependencyError
```

## KlovisError

Base exception class for all Klovis-specific errors.

```python
class KlovisError(Exception):
    """Base exception class for all Klovis errors."""
    pass
```

All other Klovis exceptions inherit from this class.

## MissingAPIKeyError

Raised when a required API key is missing or invalid.

```python
class MissingAPIKeyError(KlovisError):
    """Raised when the required Klovis API key is missing or invalid."""
    pass
```

**Example:**
```python
from klovis.exceptions import MissingAPIKeyError

try:
    # Operation requiring API key
    pass
except MissingAPIKeyError as e:
    print(f"API key required: {e}")
```

## InvalidDataError

Raised when input data is invalid, corrupted, or cannot be processed.

```python
class InvalidDataError(KlovisError):
    """Raised when input data is invalid, corrupted, or cannot be processed."""
    pass
```

**Example:**
```python
from klovis.exceptions import InvalidDataError

try:
    # Data processing
    pass
except InvalidDataError as e:
    print(f"Invalid data: {e}")
```

## ProcessingError

Raised when an internal processing step fails.

```python
class ProcessingError(KlovisError):
    """Raised when an internal processing step fails."""
    pass
```

**Example:**
```python
from klovis.exceptions import ProcessingError

try:
    pipeline.run(sources)
except ProcessingError as e:
    print(f"Processing failed: {e}")
```

## ModuleDependencyError

Raised when a module depends on unavailable external libraries or models.

```python
class ModuleDependencyError(KlovisError):
    """Raised when a module depends on unavailable external libraries or models."""
    pass
```

**Example:**
```python
from klovis.exceptions import ModuleDependencyError

try:
    # Operation requiring external dependency
    pass
except ModuleDependencyError as e:
    print(f"Missing dependency: {e}")
```

## Error Handling Best Practices

1. **Catch specific exceptions**: Handle each exception type appropriately
2. **Log errors**: Use logging to track errors in production
3. **Provide context**: Include helpful error messages
4. **Graceful degradation**: Continue processing when possible

**Example:**
```python
from klovis.exceptions import KlovisError, ProcessingError

try:
    result = pipeline.run(sources)
except ProcessingError as e:
    logger.error(f"Pipeline failed: {e}")
    # Handle error
except KlovisError as e:
    logger.error(f"Klovis error: {e}")
    # Handle general Klovis error
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Handle unexpected errors
```

