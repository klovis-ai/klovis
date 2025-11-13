from klovis.pipeline import KlovisPipeline
from klovis.loaders import DocumentLoader
from klovis.cleaning import TextCleaner
from klovis.chunking import SimpleChunker
from klovis.metadata import MetadataGenerator

pipeline = KlovisPipeline(
    loader=DocumentLoader(),
    cleaner=TextCleaner(),
    chunker=SimpleChunker(),
    metadata_generator=MetadataGenerator(),
    export_results=True,
    export_format="parquet"
)

results = pipeline.run(["my_document.pdf"])
