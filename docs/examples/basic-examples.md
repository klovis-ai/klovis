# Basic Examples

Simple, practical examples to get you started with Klovis.

## Loading Documents

### Load from Directory

```python
from klovis.loaders import DirectoryLoader

loader = DirectoryLoader(path="data/", recursive=True)
documents = loader.load()
print(f"Loaded {len(documents)} documents")
```

### Load Single Text File

```python
from klovis.loaders import TextFileLoader

loader = TextFileLoader("document.txt")
documents = loader.load(["document.txt"])
```

### Load HTML File

```python
from klovis.loaders import HTMLLoader

loader = HTMLLoader(path="page.html", markdownify=True)
documents = loader.load()
```

## Cleaning Text

### Basic Cleaning

```python
from klovis.cleaning import TextCleaner, NormalizeCleaner
from klovis.models import Document

doc = Document(source="test.txt", content="HELLO   WORLD!")
cleaner = TextCleaner()
cleaned = cleaner.clean([doc])[0]
print(cleaned.content)  # "HELLO WORLD!"
```

### Cleaning Pipeline

```python
from klovis.cleaning import CompositeCleaner, HTMLCleaner, TextCleaner

pipeline = CompositeCleaner([
    HTMLCleaner(),
    TextCleaner(),
])
cleaned = pipeline.clean(documents)
```

## Chunking Documents

### Simple Chunking

```python
from klovis.chunking import SimpleChunker

chunker = SimpleChunker(chunk_size=500, chunk_overlap=50)
chunks = chunker.chunk(documents)
```

### Markdown Chunking

```python
from klovis.chunking import MarkdownChunker

chunker = MarkdownChunker(max_chunk_size=1500, overlap=150)
chunks = chunker.chunk(documents)
```

## Complete Workflow

```python
from klovis.loaders import DirectoryLoader
from klovis.cleaning import CompositeCleaner, HTMLCleaner, TextCleaner
from klovis.chunking import SimpleChunker

# Load
loader = DirectoryLoader(path="data/")
documents = loader.load()

# Clean
cleaner = CompositeCleaner([HTMLCleaner(), TextCleaner()])
cleaned = cleaner.clean(documents)

# Chunk
chunker = SimpleChunker(chunk_size=1000)
chunks = chunker.chunk(cleaned)

print(f"Processed {len(documents)} documents into {len(chunks)} chunks")
```

