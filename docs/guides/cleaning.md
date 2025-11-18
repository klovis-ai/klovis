# Cleaning Guide

Cleaning is the process of normalizing and sanitizing document text before chunking and indexing.

## Overview

Klovis provides several cleaners for different text normalization tasks:

- **HTMLCleaner**: Remove HTML tags and extract text
- **TextCleaner**: Normalize whitespace and special characters
- **NormalizeCleaner**: Unicode normalization and case conversion
- **EmojiCleaner**: Handle emoji characters
- **CompositeCleaner**: Chain multiple cleaners together

## HTMLCleaner

Removes HTML tags and extracts clean text content.

### Basic Usage

```python
from klovis.cleaning import HTMLCleaner
from klovis.models import Document

doc = Document(
    source="page.html",
    content="<html><body><h1>Title</h1><p>Content</p></body></html>"
)

cleaner = HTMLCleaner()
cleaned = cleaner.clean([doc])[0]

print(cleaned.content)  # "Title\nContent"
```

### Features

- Removes `<script>`, `<style>`, and `<noscript>` tags
- Extracts text while preserving structure
- Handles malformed HTML gracefully

## TextCleaner

Normalizes whitespace and removes special characters.

### Basic Usage

```python
from klovis.cleaning import TextCleaner

doc = Document(
    source="text.txt",
    content="This   has    multiple    spaces.\n\nAnd   newlines."
)

cleaner = TextCleaner()
cleaned = cleaner.clean([doc])[0]

print(cleaned.content)  # Normalized text
```

### Features

- Collapses multiple spaces
- Normalizes line breaks
- Removes control characters
- Handles Unicode whitespace

## NormalizeCleaner

Performs Unicode normalization and case conversion.

### Basic Usage

```python
from klovis.cleaning import NormalizeCleaner

doc = Document(
    source="text.txt",
    content="HELLO World! This is a TÉST."
)

# Lowercase conversion
cleaner = NormalizeCleaner(lowercase=True, preserve_newlines=True)
cleaned = cleaner.clean([doc])[0]

print(cleaned.content)  # "hello world! this is a tést."
```

### Parameters

- `lowercase` (bool): Convert to lowercase (default: False)
- `preserve_newlines` (bool): Keep newline characters (default: True)

### Features

- Unicode normalization (NFD/NFC)
- Case conversion
- Preserves document structure

## EmojiCleaner

Handles emoji characters in text.

### Basic Usage

```python
from klovis.cleaning import EmojiCleaner

doc = Document(
    source="text.txt",
    content="Hello! 🎉 This is great! 🚀"
)

# Remove emojis
cleaner = EmojiCleaner(replace=False)
cleaned = cleaner.clean([doc])[0]

print(cleaned.content)  # "Hello!  This is great! "
```

### Parameters

- `replace` (bool): If True, replaces emojis with text descriptions (default: False)

## CompositeCleaner

Chain multiple cleaners together for a complete cleaning pipeline.

### Basic Usage

```python
from klovis.cleaning import (
    HTMLCleaner,
    TextCleaner,
    NormalizeCleaner,
    EmojiCleaner,
    CompositeCleaner,
)

# Create a cleaning pipeline
pipeline = CompositeCleaner([
    HTMLCleaner(),  # Remove HTML first
    TextCleaner(),  # Normalize whitespace
    NormalizeCleaner(lowercase=True),  # Convert to lowercase
    EmojiCleaner(replace=False),  # Remove emojis
])

documents = pipeline.clean(documents)
```

### Execution Order

Cleaners are executed in the order they're added to the list. Order matters!

**Recommended order:**
1. HTMLCleaner (if HTML present)
2. TextCleaner (normalize whitespace)
3. NormalizeCleaner (case conversion)
4. EmojiCleaner (emoji handling)

## Common Patterns

### Basic Text Cleaning

```python
from klovis.cleaning import TextCleaner, NormalizeCleaner, CompositeCleaner

cleaner = CompositeCleaner([
    TextCleaner(),
    NormalizeCleaner(lowercase=True),
])
```

### HTML Document Cleaning

```python
from klovis.cleaning import HTMLCleaner, TextCleaner, CompositeCleaner

cleaner = CompositeCleaner([
    HTMLCleaner(),
    TextCleaner(),
])
```

### Production-Ready Pipeline

```python
from klovis.cleaning import (
    HTMLCleaner,
    TextCleaner,
    NormalizeCleaner,
    EmojiCleaner,
    CompositeCleaner,
)

cleaner = CompositeCleaner([
    HTMLCleaner(),
    TextCleaner(),
    NormalizeCleaner(lowercase=True, preserve_newlines=True),
    EmojiCleaner(replace=False),
])
```

## Custom Cleaners

Create custom cleaners by inheriting from `BaseCleaner`:

```python
from klovis.base import BaseCleaner
from klovis.models import Document
from typing import List

class CustomCleaner(BaseCleaner):
    def clean(self, documents: List[Document]) -> List[Document]:
        cleaned = []
        for doc in documents:
            # Your cleaning logic here
            cleaned_content = doc.content.upper()  # Example
            cleaned_doc = Document(
                source=doc.source,
                content=cleaned_content,
                metadata=doc.metadata
            )
            cleaned.append(cleaned_doc)
        return cleaned
```

## Best Practices

1. **Order matters**: Apply cleaners in logical order (HTML → Text → Normalize)
2. **Preserve structure**: Use `preserve_newlines=True` when structure matters
3. **Test incrementally**: Test each cleaner individually before combining
4. **Handle edge cases**: Empty documents, special characters, etc.
5. **Preserve metadata**: Don't lose important metadata during cleaning

## Performance Tips

- **Batch processing**: Cleaners process lists efficiently
- **Early filtering**: Remove empty documents before cleaning
- **Selective cleaning**: Only use necessary cleaners for your use case

## Next Steps

- Learn about [Chunking](chunking.md) to split cleaned documents
- See [API Reference](../api/cleaners.md) for complete API documentation
- Check [Examples](../examples/) for cleaning patterns

