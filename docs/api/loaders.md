# Loaders API Reference

Complete API documentation for all loader classes.

## DirectoryLoader

Loads multiple document types from a directory structure.

### Class Definition

```python
class DirectoryLoader(BaseLoader):
    def __init__(
        self,
        path: str,
        recursive: bool = True,
        ignore_hidden: bool = True,
        markdownify: bool = False,
    )
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str` | Required | Path to the directory to load |
| `recursive` | `bool` | `True` | If True, loads files from subdirectories |
| `ignore_hidden` | `bool` | `True` | If True, skips hidden files/directories |
| `markdownify` | `bool` | `False` | If True, converts HTML/PDF to Markdown |

### Methods

#### `load() -> List[Document]`

Loads all supported files from the directory.

**Returns:**
- `List[Document]`: List of loaded documents

**Raises:**
- `FileNotFoundError`: If the directory doesn't exist

**Example:**
```python
loader = DirectoryLoader(path="data/", recursive=True)
documents = loader.load()
```

### Supported File Types

- `.txt` - Text files
- `.html`, `.htm` - HTML files
- `.pdf` - PDF documents
- `.json` - JSON files

---

## TextFileLoader

Loads plain text files.

### Class Definition

```python
class TextFileLoader(BaseLoader):
    def __init__(self, path: str)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str` | Required | Path to the text file |

### Methods

#### `load(sources: List[str]) -> List[Document]`

Loads text files from the provided sources.

**Parameters:**
- `sources` (`List[str]`): List of file paths to load

**Returns:**
- `List[Document]`: List of loaded documents

**Example:**
```python
loader = TextFileLoader("example.txt")
documents = loader.load(["example.txt"])
```

---

## HTMLLoader

Loads and parses HTML files.

### Class Definition

```python
class HTMLLoader(BaseLoader):
    def __init__(
        self,
        path: str,
        markdownify: bool = False,
    )
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str` | Required | Path to HTML file or directory |
| `markdownify` | `bool` | `False` | If True, converts HTML to Markdown |

### Methods

#### `load() -> List[Document]`

Loads HTML files and extracts text content.

**Returns:**
- `List[Document]`: List of loaded documents with `format` in metadata

**Raises:**
- `FileNotFoundError`: If the path doesn't exist

**Example:**
```python
loader = HTMLLoader(path="page.html", markdownify=True)
documents = loader.load()
```

---

## JSONLoader

Loads text data from JSON files.

### Class Definition

```python
class JSONLoader(BaseLoader):
    def __init__(
        self,
        path: str,
        text_field: str = "content",
    )
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str` | Required | Path to JSON file |
| `text_field` | `str` | `"content"` | JSON key to extract text from |

### Methods

#### `load() -> List[Document]`

Loads text data from JSON file.

**Returns:**
- `List[Document]`: List of loaded documents

**Raises:**
- `FileNotFoundError`: If the file doesn't exist

**Example:**
```python
loader = JSONLoader(path="data.json", text_field="text")
documents = loader.load()
```

---

## PDFLoader

Extracts text from PDF documents.

### Class Definition

```python
class PDFLoader(BaseLoader):
    def __init__(self, path: str)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str` | Required | Path to PDF file |

### Methods

#### `load() -> List[Document]`

Extracts text from PDF file.

**Returns:**
- `List[Document]`: List of loaded documents with page count in metadata

**Raises:**
- `FileNotFoundError`: If the file doesn't exist

**Example:**
```python
loader = PDFLoader(path="document.pdf")
documents = loader.load()
```

**Requirements:**
- Requires `pypdf` or `pdfplumber` package

---

## BaseLoader

Abstract base class for all loaders.

### Class Definition

```python
class BaseLoader(ABC):
    @abstractmethod
    def load(self, sources: List[str]) -> List[Document]:
        pass
```

### Creating Custom Loaders

```python
from klovis.base import BaseLoader
from klovis.models import Document
from typing import List

class CustomLoader(BaseLoader):
    def load(self, sources: List[str]) -> List[Document]:
        documents = []
        for source in sources:
            # Your loading logic
            doc = Document(source=source, content="...")
            documents.append(doc)
        return documents
```

