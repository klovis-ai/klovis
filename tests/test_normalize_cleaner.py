from klovis.cleaning.normalize_cleaner import NormalizeCleaner
from klovis.models import Document

def test_normalize_cleaner_typography():
    cleaner = NormalizeCleaner()
    text = '“Hello”—said the man…  It’s  l’affaire française.'
    doc = Document(source="test.txt", content=text)

    cleaned = cleaner.clean([doc])[0]
    

    assert '"' in cleaned.content
    assert ". . ." in cleaned.content
    assert "-" in cleaned.content
    assert "'" in cleaned.content
    assert "francaise" not in cleaned.content  # accents preserved
    assert "  " not in cleaned.content
