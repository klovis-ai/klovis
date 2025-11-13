from klovis.transforming.markdown_transformer import MarkdownTransformer
from klovis.models import Chunk

def test_markdown_transformer_output():
    chunks = [
        Chunk(text="Hello Klovis", metadata={"chunk_id": 0, "source": "test.txt"})
    ]
    transformer = MarkdownTransformer()
    md = transformer.transform(chunks)
    
    print(md[0])

    assert "## Source:" in md[0]["markdown"]
    assert "**Content:**" in md[0]["markdown"]
    assert "Hello Klovis" in md[0]["markdown"]
