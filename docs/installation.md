# Installation Guide

This guide will help you install Klovis and its dependencies.

## Requirements

- Python 3.8 or higher
- pip or Poetry for package management

## Basic Installation

Install Klovis from PyPI:

```bash
pip install klovis
```

## Installation with Poetry

If you're using Poetry for dependency management:

```bash
poetry add klovis
```

## Optional Dependencies

Klovis has optional dependencies for specific features:

### PDF Support

To enable PDF loading capabilities:

```bash
pip install klovis[pdf]
# or
pip install pypdf
```

### Enhanced Features

For all optional dependencies:

```bash
pip install klovis[all]
```

This includes:
- PDF processing libraries
- Additional text processing utilities
- Enhanced cleaning capabilities

## Development Installation

To install Klovis in development mode with all dependencies:

```bash
git clone https://github.com/klovis-ai/klovis.git
cd klovis
pip install -e ".[dev,all]"
```

This installs:
- Klovis in editable mode
- Development dependencies (pytest, black, etc.)
- All optional features

## Verification

Verify your installation:

```python
import klovis
print(klovis.__version__)

# Test basic functionality
from klovis.loaders import DirectoryLoader
from klovis.models import Document

print("✅ Klovis installed successfully!")
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you're using the correct Python version:

```bash
python --version  # Should be 3.8+
```

### Missing Dependencies

If specific features don't work, install the required dependencies:

```bash
# For PDF support
pip install pypdf

# For HTML processing
pip install beautifulsoup4 markdownify

# For advanced text processing
pip install unidecode
```

### Virtual Environment

It's recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install Klovis
pip install klovis
```

## Next Steps

Once installed, check out the [Quick Start Guide](quickstart.md) to get started with Klovis.

