from klovis.cleaning.text_cleaner import TextCleaner
from klovis.models import Document

def test_text_cleaner_normalization():
    cleaner = TextCleaner()

    docs = [
        Document(source="doc1.txt", content="Hello   world!   This  is  Klovis."),
        Document(source="doc2.txt", content="\nAnother   document   here.  ")
    ]

    cleaned_docs = cleaner.clean(docs)

    assert isinstance(cleaned_docs[0], Document)
    assert cleaned_docs[0].content == "Hello world! This is Klovis."
    assert cleaned_docs[1].content == "Another document here."
