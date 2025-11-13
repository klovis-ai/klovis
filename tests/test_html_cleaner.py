from klovis.cleaning.html_cleaner import HTMLCleaner
from klovis.models import Document

def test_html_cleaner_removes_tags_and_entities():
    cleaner = HTMLCleaner()

    html_text = """
    <html><body><h1>Title&nbsp;&amp; Test</h1>
    <p>Hello&nbsp; <b>world</b>! &#39;Klovis&#39; rocks.</p></body></html>
    """
    doc = Document(source="test.html", content=html_text)
    cleaned = cleaner.clean([doc])[0]
    assert "<" not in cleaned.content
    assert "nbsp" not in cleaned.content
    assert "Klovis" in cleaned.content
    assert "Title & Test" in cleaned.content
    assert "Hello world !" in cleaned.content
