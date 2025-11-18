# Advanced Examples

Complex examples demonstrating advanced Klovis features.

## Semantic Merging Workflow

```python
from klovis.loaders import DirectoryLoader
from klovis.cleaning import CompositeCleaner, HTMLCleaner, TextCleaner
from klovis.chunking import SimpleChunker
from klovis.merger import SemanticMerger
from your_embedder import YourEmbedder

# Load and clean
loader = DirectoryLoader(path="data/", recursive=True, markdownify=True)
documents = loader.load()

cleaner = CompositeCleaner([HTMLCleaner(), TextCleaner()])
cleaned = cleaner.clean(documents)

# Initial chunking
chunker = SimpleChunker(chunk_size=500, chunk_overlap=50)
chunks = chunker.chunk(cleaned)

# Semantic merging
embedder = YourEmbedder()
merger = SemanticMerger(
    embedder=embedder,
    max_size=2000,
    distance_threshold=0.3,
    batch_size=32,
)
merged = merger.merge(chunks)

print(f"Reduced {len(chunks)} chunks to {len(merged)} merged chunks")
```

## Custom Processing Pipeline

```python
from klovis.base import BaseCleaner, BaseChunker
from klovis.models import Document, Chunk
from typing import List
import re

class CustomCleaner(BaseCleaner):
    def clean(self, documents: List[Document]) -> List[Document]:
        cleaned = []
        for doc in documents:
            # Remove URLs
            content = re.sub(r'http\S+', '', doc.content)
            # Remove email addresses
            content = re.sub(r'\S+@\S+', '', content)
            cleaned.append(Document(
                source=doc.source,
                content=content,
                metadata=doc.metadata
            ))
        return cleaned

class SentenceChunker(BaseChunker):
    def __init__(self, sentences_per_chunk: int = 5):
        self.sentences_per_chunk = sentences_per_chunk
    
    def chunk(self, documents: List[Document]) -> List[Chunk]:
        chunks = []
        for doc in documents:
            sentences = re.split(r'[.!?]+', doc.content)
            for i in range(0, len(sentences), self.sentences_per_chunk):
                chunk_text = '. '.join(sentences[i:i+self.sentences_per_chunk])
                chunks.append(Chunk(
                    text=chunk_text,
                    metadata={"chunk_id": len(chunks), "source": doc.source}
                ))
        return chunks

# Use custom components
cleaner = CustomCleaner()
chunker = SentenceChunker(sentences_per_chunk=3)

cleaned = cleaner.clean(documents)
chunks = chunker.chunk(cleaned)
```

## Batch Processing Large Datasets

```python
from klovis.loaders import DirectoryLoader
from klovis.cleaning import TextCleaner
from klovis.chunking import SimpleChunker

loader = DirectoryLoader(path="large_dataset/")
documents = loader.load()

# Process in batches
batch_size = 100
all_chunks = []

cleaner = TextCleaner()
chunker = SimpleChunker(chunk_size=1000)

for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    cleaned = cleaner.clean(batch)
    chunks = chunker.chunk(cleaned)
    all_chunks.extend(chunks)
    
    print(f"Processed batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")

print(f"Total chunks: {len(all_chunks)}")
```

## Error-Resilient Pipeline

```python
from klovis.loaders import DirectoryLoader
from klovis.cleaning import CompositeCleaner
from klovis.chunking import SimpleChunker
from klovis.utils import get_logger

logger = get_logger(__name__)

def process_safely(documents):
    valid_docs = []
    for doc in documents:
        try:
            if not doc.content or not doc.content.strip():
                logger.warning(f"Skipping empty document: {doc.source}")
                continue
            valid_docs.append(doc)
        except Exception as e:
            logger.error(f"Error processing {doc.source}: {e}")
            continue
    
    try:
        cleaner = CompositeCleaner([TextCleaner()])
        cleaned = cleaner.clean(valid_docs)
    except Exception as e:
        logger.error(f"Cleaning failed: {e}")
        cleaned = valid_docs  # Fallback
    
    try:
        chunker = SimpleChunker(chunk_size=1000)
        chunks = chunker.chunk(cleaned)
    except Exception as e:
        logger.error(f"Chunking failed: {e}")
        # Create single chunk per document as fallback
        chunks = [Chunk(text=d.content, metadata={"source": d.source}) 
                 for d in cleaned]
    
    return chunks

loader = DirectoryLoader(path="data/")
documents = loader.load()
chunks = process_safely(documents)
```

## Metadata-Enriched Pipeline

```python
from klovis.loaders import DirectoryLoader
from klovis.cleaning import TextCleaner
from klovis.chunking import SimpleChunker
from klovis.metadata.metadata_generator import MetadataGenerator
from klovis.transforming import MarkdownTransformer

# Process documents
loader = DirectoryLoader(path="data/")
documents = loader.load()

cleaner = TextCleaner()
cleaned = cleaner.clean(documents)

chunker = SimpleChunker(chunk_size=1000)
chunks = chunker.chunk(cleaned)

# Add metadata
metadata_gen = MetadataGenerator()
enriched = metadata_gen.generate(chunks)

# Transform to Markdown
transformer = MarkdownTransformer(include_metadata=True)
markdown_output = transformer.transform(enriched)

# Save results
with open("output.md", "w") as f:
    for item in markdown_output:
        f.write(item["markdown"])
```

