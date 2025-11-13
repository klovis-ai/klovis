from klovis.loaders.pdf_loader import PDFLoader
from klovis.models import Document
from pathlib import Path

def test_pdf_loader(tmp_path):
    # Create a fake minimal PDF file (pdfplumber still parses empty ones)
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%EOF\n")

    loader = PDFLoader(path=pdf_path)
    docs = loader.load()

    # Should handle gracefully even if PDF is empty
    assert isinstance(docs, list)
    assert all(isinstance(d, Document) for d in docs) or len(docs) == 0
