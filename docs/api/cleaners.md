# Cleaners API Reference

Complete API documentation for all cleaner classes.

## HTMLCleaner

Removes HTML tags and extracts clean text content.

### Class Definition

```python
class HTMLCleaner(BaseCleaner):
    def clean(self, documents: List[Document]) -> List[Document]
```

### Methods

#### `clean(documents: List[Document]) -> List[Document]`

Removes HTML tags and extracts text.

**Parameters:**
- `documents` (`List[Document]`): Documents to clean

**Returns:**
- `List[Document]`: Cleaned documents

**Features:**
- Removes `<script>`, `<style>`, and `<noscript>` tags
- Extracts text while preserving structure
- Handles malformed HTML gracefully

**Example:**
```python
from klovis.cleaning import HTMLCleaner

cleaner = HTMLCleaner()
cleaned = cleaner.clean(documents)
```

---

## TextCleaner

Normalizes whitespace and removes special characters.

### Class Definition

```python
class TextCleaner(BaseCleaner):
    def clean(self, documents: List[Document]) -> List[Document]
```

### Methods

#### `clean(documents: List[Document]) -> List[Document]`

Normalizes text content.

**Parameters:**
- `documents` (`List[Document]`): Documents to clean

**Returns:**
- `List[Document]`: Cleaned documents

**Features:**
- Collapses multiple spaces
- Normalizes line breaks
- Removes control characters
- Handles Unicode whitespace

**Example:**
```python
from klovis.cleaning import TextCleaner

cleaner = TextCleaner()
cleaned = cleaner.clean(documents)
```

---

## NormalizeCleaner

Performs Unicode normalization and case conversion.

### Class Definition

```python
class NormalizeCleaner(BaseCleaner):
    def __init__(
        self,
        lowercase: bool = False,
        preserve_newlines: bool = True,
    )
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `lowercase` | `bool` | `False` | Convert text to lowercase |
| `preserve_newlines` | `bool` | `True` | Preserve newline characters |

### Methods

#### `clean(documents: List[Document]) -> List[Document]`

Normalizes document text.

**Parameters:**
- `documents` (`List[Document]`): Documents to normalize

**Returns:**
- `List[Document]`: Normalized documents

**Example:**
```python
from klovis.cleaning import NormalizeCleaner

cleaner = NormalizeCleaner(lowercase=True, preserve_newlines=True)
cleaned = cleaner.clean(documents)
```

---

## EmojiCleaner

Handles emoji characters in text.

### Class Definition

```python
class EmojiCleaner(BaseCleaner):
    def __init__(self, replace: bool = False)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `replace` | `bool` | `False` | If True, replaces emojis with text descriptions |

### Methods

#### `clean(documents: List[Document]) -> List[Document]`

Removes or replaces emojis.

**Parameters:**
- `documents` (`List[Document]`): Documents to clean

**Returns:**
- `List[Document]`: Cleaned documents

**Example:**
```python
from klovis.cleaning import EmojiCleaner

# Remove emojis
cleaner = EmojiCleaner(replace=False)
cleaned = cleaner.clean(documents)
```

---

## CompositeCleaner

Chains multiple cleaners together.

### Class Definition

```python
class CompositeCleaner(BaseCleaner):
    def __init__(self, cleaners: List[BaseCleaner])
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cleaners` | `List[BaseCleaner]` | Required | List of cleaner instances to apply in order |

### Methods

#### `clean(documents: List[Document]) -> List[Document]`

Applies all cleaners sequentially.

**Parameters:**
- `documents` (`List[Document]`): Documents to clean

**Returns:**
- `List[Document]`: Cleaned documents

**Example:**
```python
from klovis.cleaning import CompositeCleaner, HTMLCleaner, TextCleaner

pipeline = CompositeCleaner([
    HTMLCleaner(),
    TextCleaner(),
])
cleaned = pipeline.clean(documents)
```

---

## BaseCleaner

Abstract base class for all cleaners.

### Class Definition

```python
class BaseCleaner(ABC):
    @abstractmethod
    def clean(self, documents: List[Document]) -> List[Document]:
        pass
```

### Creating Custom Cleaners

```python
from klovis.base import BaseCleaner
from klovis.models import Document
from typing import List

class CustomCleaner(BaseCleaner):
    def clean(self, documents: List[Document]) -> List[Document]:
        cleaned = []
        for doc in documents:
            # Your cleaning logic
            cleaned_content = doc.content.upper()
            cleaned_doc = Document(
                source=doc.source,
                content=cleaned_content,
                metadata=doc.metadata
            )
            cleaned.append(cleaned_doc)
        return cleaned
```

