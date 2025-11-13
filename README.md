<div align="center">
  <picture>
    <img alt="Klovis Logo" src=".github/images/logo.svg" width="80%">
  </picture>
</div>

<div align="center">
  <h3>The framework for unified document processing pipelines.</h3>
</div>

<div align="center">
  <a href="https://opensource.org/licenses/MIT" target="_blank"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="#" target="_blank"><img src="https://img.shields.io/badge/pypi-klovis-blue.svg" alt="PyPI"></a>
  <a href="#" target="_blank"><img src="https://img.shields.io/badge/version-latest-lightgrey.svg" alt="Version"></a>
  <a href="#" target="_blank"><img src="https://img.shields.io/badge/build-passing-brightgreen.svg" alt="Build"></a>
</div>

Klovis is a modular framework for loading, cleaning, chunking and transforming heterogeneous documents for Retrieval-Augmented Generation pipelines. It provides consistent abstractions and production-ready components so that developers can build robust data ingestion workflows without dealing with low-level parsing or text normalization details.

```bash
pip install klovis
```

---

**Documentation**:

- Official documentation: incoming
- API reference: incoming

**Discussions**: Community channels will be published soon.

## Why use Klovis?

Klovis provides a structured approach to transforming unstructured data into RAG-ready chunks. It helps developers build reliable preprocessing pipelines using standardized modules for each stage of document handling.

Use Klovis for:

- Consistent document ingestion. Load text, HTML, JSON, PDF, or an entire directory tree using a unified API. Integrations preserve metadata and ensure predictable output formats across sources.
- Robust text cleaning. Apply standardized cleaning pipelines including HTML stripping, Unicode normalization, emoji removal, and whitespace correction. Each cleaner is modular and composable.
- Flexible chunking strategies. Split documents using Markdown headings, character windows, paragraphs or other strategies. Merge chunks intelligently while respecting size constraints.
- Structured transformations. Convert processed chunks into Markdown or custom output structures for storage, indexing or model ingestion.
- Extensibility. Every module in Klovis inherits from a base abstraction, allowing developers to extend or replace behaviors with minimal friction.
- Reproducible pipelines. Implement deterministic preprocessing flows that remain stable across formats and document structures.

## Klovis ecosystem

Although Klovis can be used as a standalone preprocessing framework, it integrates naturally with downstream components in a RAG workflow.

Pair Klovis with:

- Vector databases such as FAISS, Weaviate or Chroma for chunk storage.
- Embedding models for encoding processed text.
- LLM frameworks for querying indexed content.
- Orchestration tools for pipeline automation.

Klovis focuses exclusively on document ingestion, empowering other layers of the stack with clean, structured and consistent input.

## Installation

```bash
pip install klovis
```

Or with Poetry:

```bash
poetry add klovis
```

## Quick Start

```python
from klovis.loaders import DirectoryLoader
from klovis.cleaning import HTMLCleaner, TextCleaner
from klovis.chunking import MarkdownChunker
from klovis.transforming import MarkdownTransformer

loader = DirectoryLoader(path="data/", recursive=True)
documents = loader.load()

cleaner = HTMLCleaner()
documents = cleaner.clean(documents)

chunker = MarkdownChunker(max_chunk_size=1200)
chunks = chunker.chunk(documents)

transformer = MarkdownTransformer()
output = transformer.transform(chunks)
```

## Project structure

```
klovis/
    base/                 Base interfaces for loaders, cleaners, chunkers, transformers
    loaders/              Format-specific document loaders
    cleaning/             Cleaning and normalization utilities
    chunking/             Document chunking strategies
    transforming/         Output formatting and transformation modules
    models/               Core data structures for documents and chunks
    utils/                Logging and shared helpers
    tests/                Test suite
```

## Running tests

```bash
pytest
```

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes and update or add tests.
4. Submit a pull request with a clear explanation of the modification.

## License

This project is released under the MIT License.
