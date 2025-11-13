from klovis.cleaning.text_cleaner import TextCleaner
from klovis.models import Document

def test_text_cleaner_basic():
    cleaner = TextCleaner()
    docs = [Document(source="test.txt", content="Hello   world!!   This   is\n\nKlovis.   ")]
    result = cleaner.clean(docs)

    assert len(result) == 1
    assert "Hello world!" in result[0].content
