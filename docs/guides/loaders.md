# Loaders Guide

Loaders are responsible for reading documents from various sources and converting them into `Document` objects.

## Overview

Klovis provides several loaders for different document sources:

- **DirectoryLoader**: Load multiple files from a directory
- **TextFileLoader**: Load plain text files
- **HTMLLoader**: Load and parse HTML files
- **JSONLoader**: Load structured data from JSON files
- **PDFLoader**: Extract text from PDF documents

## DirectoryLoader

Load all supported files from a directory structure.

### Basic Usage

```python
from klovis.loaders import DirectoryLoader

loader = DirectoryLoader(
    path="data/",
    recursive=True,  # Include subdirectories
    ignore_hidden=True,  # Skip hidden files
    markdownify=True,  # Convert HTML/PDF to Markdown
)

documents = loader.load()
```

### Parameters

- `path` (str): Path to the directory
- `recursive` (bool): If True, loads files from subdirectories (default: True)
- `ignore_hidden` (bool): If True, skips hidden files/directories (default: True)
- `markdownify` (bool): If True, converts HTML/PDF to Markdown (default: False)

### Supported Formats

- `.txt` - Text files
- `.html`, `.htm` - HTML files
- `.pdf` - PDF documents
- `.json` - JSON files

## TextFileLoader

Load plain text files.

### Basic Usage

```python
from klovis.loaders import TextFileLoader

loader = TextFileLoader("document.txt")
documents = loader.load(["document.txt"])
```

### Parameters

- `path` (str): Path to the text file

## HTMLLoader

Load and parse HTML files with optional Markdown conversion.

### Basic Usage

```python
from klovis.loaders import HTMLLoader

# Load as plain text
loader = HTMLLoader(path="page.html", markdownify=False)
documents = loader.load()

# Load and convert to Markdown
loader = HTMLLoader(path="page.html", markdownify=True)
documents = loader.load()
```

### Parameters

- `path` (str): Path to HTML file or directory
- `markdownify` (bool): If True, converts HTML to Markdown (default: False)

### Features

- Removes scripts, styles, and noscript tags
- Extracts clean text content
- Optional Markdown conversion for better structure

## JSONLoader

Load text data from JSON files.

### Basic Usage

```python
from klovis.loaders import JSONLoader

# Load from a single JSON file
loader = JSONLoader(path="data.json", text_field="content")
documents = loader.load()
```

### Parameters

- `path` (str): Path to JSON file
- `text_field` (str): JSON key to extract text from (default: "content")

### Supported Structures

**Single Object:**
```json
{
  "content": "Text content here",
  "metadata": {...}
}
```

**Array of Objects:**
```json
[
  {"content": "First item"},
  {"content": "Second item"}
]
```

## PDFLoader

Extract text from PDF documents.

### Basic Usage

```python
from klovis.loaders import PDFLoader

loader = PDFLoader(path="document.pdf")
documents = loader.load()
```

### Parameters

- `path` (str): Path to PDF file

### Requirements

Requires `pypdf` package:
```bash
pip install pypdf
```

## Error Handling

All loaders raise `FileNotFoundError` if the specified path doesn't exist:

```python
from klovis.loaders import TextFileLoader

try:
    loader = TextFileLoader("nonexistent.txt")
    documents = loader.load(["nonexistent.txt"])
except FileNotFoundError as e:
    print(f"File not found: {e}")
```

## Custom Loaders

Create custom loaders by inheriting from `BaseLoader`:

```python
from klovis.base import BaseLoader
from klovis.models import Document

class CustomLoader(BaseLoader):
    def load(self, sources):
        documents = []
        for source in sources:
            # Your loading logic here
            doc = Document(source=source, content="...")
            documents.append(doc)
        return documents
```

## Best Practices

1. **Use DirectoryLoader** for batch processing multiple files
2. **Enable markdownify** for HTML/PDF to preserve structure
3. **Handle errors** gracefully in production code
4. **Preserve metadata** when creating custom loaders
5. **Use appropriate loaders** for each file type

## Next Steps

- Learn about [Cleaning](cleaning.md) to process loaded documents
- See [API Reference](../api/loaders.md) for complete API documentation
- Check [Examples](../examples/) for usage patterns

