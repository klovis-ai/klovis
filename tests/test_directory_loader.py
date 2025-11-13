from klovis.loaders.directory_loader import DirectoryLoader
from klovis.models import Document
from pathlib import Path
import json

def test_directory_loader_with_multiple_formats(tmp_path):
    # --- Setup test directory
    subdir = tmp_path / "nested"
    subdir.mkdir()

    # Create text file
    txt_file = tmp_path / "doc1.txt"
    txt_file.write_text("Hello Klovis from text file.")

    # Create JSON file
    json_file = tmp_path / "data.json"
    json_file.write_text(json.dumps({"content": "JSON data for Klovis"}))

    # Create HTML file
    html_file = subdir / "page.html"
    html_file.write_text("<html><body><h1>Hello Klovis</h1></body></html>")

    # Simulate empty PDF file (can't actually generate real PDF easily in tmp)
    pdf_file = subdir / "empty.pdf"
    pdf_file.write_text("%PDF-1.4\n%Fake minimal PDF for testing\n")

    # --- Run loader
    loader = DirectoryLoader(path=str(tmp_path), recursive=True)
    documents = loader.load()
    print(f"========================================{len(documents)}")
    print(documents)

    # --- Assertions
    assert isinstance(documents, list)
    assert all(isinstance(d, Document) for d in documents)
    assert len(documents) >= 3  # Should load at least txt, json, html
    sources = [d.source for d in documents]
    assert any("doc1.txt" in s for s in sources)
    assert any("data.json" in s for s in sources)
    assert any("page.html" in s for s in sources)


def test_directory_loader_empty(tmp_path):
    loader = DirectoryLoader(path=str(tmp_path))
    docs = loader.load()
    assert docs == []