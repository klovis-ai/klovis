from klovis.loaders.text_file_loader import TextFileLoader
from klovis.models import Document
from pathlib import Path

def test_text_file_loader(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("Hello Klovis!")

    loader = TextFileLoader(path=file_path)
    docs = loader.load()

    assert len(docs) == 1
    assert isinstance(docs[0], Document)
    assert docs[0].content == "Hello Klovis!"
