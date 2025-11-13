from klovis.pipeline.pipeline import KlovisPipeline
from klovis.loaders.document_loader import DocumentLoader
from klovis.cleaning.text_cleaner import TextCleaner
from klovis.chunking.simple_chunker import SimpleChunker
from klovis.metadata.metadata_generator import MetadataGenerator
from klovis.models import Chunk

def test_pipeline_end_to_end():
    pipeline = KlovisPipeline(
        loader=DocumentLoader(),
        cleaner=TextCleaner(),
        chunker=SimpleChunker(),
        metadata_generator=MetadataGenerator(),
        require_api_key=False
    )

    results = pipeline.run(["file.txt"])

    assert len(results) > 0
    first = results[0]

    assert isinstance(first, Chunk)
    assert isinstance(first.metadata, dict)
    assert "length" in first.metadata
    assert "tags" in first.metadata
