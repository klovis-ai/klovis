


class MetadataPipeline:
    def __init__(self, generators):
        self.generators = generators

    def apply(self, chunks):
        for chunk in chunks:
            for generator in self.generators:
                meta = generator.generate(chunk)
                if meta:
                    chunk.metadata.update(meta)
        return chunks
