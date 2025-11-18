from klovis.loaders.html_loader import HTMLLoader
from klovis.models import Document
from pathlib import Path
import tempfile
import os


def test_html_loader_basic():
    """Test loading a simple HTML file."""
    html_content = """
    <html>
        <head><title>Test</title></head>
        <body>
            <h1>Hello World</h1>
            <p>This is a test paragraph.</p>
        </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_path = f.name
    
    try:
        loader = HTMLLoader(path=temp_path, markdownify=False)
        docs = loader.load()
        
        assert len(docs) == 1
        assert isinstance(docs[0], Document)
        assert docs[0].source == temp_path
        assert "Hello World" in docs[0].content
        assert docs[0].metadata.get("format") == "html"
    finally:
        os.unlink(temp_path)


def test_html_loader_markdownify():
    """Test HTML to Markdown conversion."""
    html_content = """
    <html>
        <body>
            <h1>Title</h1>
            <p>Paragraph</p>
        </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_path = f.name
    
    try:
        loader = HTMLLoader(path=temp_path, markdownify=True)
        docs = loader.load()
        
        assert len(docs) == 1
        assert docs[0].metadata.get("format") == "markdown"
    finally:
        os.unlink(temp_path)


def test_html_loader_not_found():
    """Test error handling for non-existent file."""
    loader = HTMLLoader(path="file42.html")
    
    try:
        loader.load()
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass

