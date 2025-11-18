# Models API Reference

Complete API documentation for data models.

## Document

Represents a raw or loaded document.

### Class Definition

```python
class Document(KlovisBaseModel):
    source: Any
    content: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `source` | `Any` | Document source (path, URL, or identifier) |
| `content` | `str` | Document text content |
| `metadata` | `Dict[str, Any]` | Additional metadata (default: `{}`) |

### Methods

#### `to_dict() -> Dict[str, Any]`

Converts the document to a dictionary.

**Returns:**
- `Dict[str, Any]`: Dictionary representation

**Example:**
```python
doc = Document(source="test.txt", content="Content")
doc_dict = doc.to_dict()
```

#### `to_json(indent: int = 2) -> str`

Converts the document to a JSON string.

**Parameters:**
- `indent` (`int`): Number of spaces for indentation (default: 2)

**Returns:**
- `str`: JSON string representation

**Example:**
```python
json_str = doc.to_json(indent=4)
```

### Example

```python
from klovis.models import Document

doc = Document(
    source="example.txt",
    content="Document content here",
    metadata={"author": "John Doe", "date": "2024-01-01"}
)

print(doc.source)  # "example.txt"
print(doc.content)  # "Document content here"
print(doc.metadata)  # {"author": "John Doe", "date": "2024-01-01"}
```

---

## Chunk

Represents a processed chunk of text.

### Class Definition

```python
class Chunk(KlovisBaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `text` | `str` | Chunk text content |
| `metadata` | `Dict[str, Any]` | Processing metadata (default: `{}`) |

### Methods

#### `to_dict() -> Dict[str, Any]`

Converts the chunk to a dictionary.

**Returns:**
- `Dict[str, Any]`: Dictionary representation

#### `to_json(indent: int = 2) -> str`

Converts the chunk to a JSON string.

**Parameters:**
- `indent` (`int`): Number of spaces for indentation (default: 2)

**Returns:**
- `str`: JSON string representation

### Common Metadata Fields

Chunks typically include:
- `chunk_id`: Sequential identifier
- `source`: Source document path
- `length`: Character count
- `type`: Chunk type (e.g., "simple", "markdown", "semantic")

### Example

```python
from klovis.models import Chunk

chunk = Chunk(
    text="Chunk content here",
    metadata={
        "chunk_id": 0,
        "source": "doc.txt",
        "length": 18,
        "type": "simple"
    }
)

print(chunk.text)  # "Chunk content here"
print(chunk.metadata["chunk_id"])  # 0
```

---

## KlovisBaseModel

Base class for all Klovis models (Document, Chunk).

### Features

- Pydantic-based validation
- Type safety
- Serialization methods (`to_dict()`, `to_json()`)
- Metadata preservation

### Configuration

- `arbitrary_types_allowed = True`
- `validate_assignment = True`
- `extra = "forbid"` (prevents extra fields)
- `frozen = False` (mutable models)
- `str_strip_whitespace = True`

