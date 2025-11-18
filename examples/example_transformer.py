"""
Exemple d'utilisation des transformers de Klovis.

Les transformers convertissent les chunks en différents formats
pour l'export ou l'indexation.
"""

from klovis.models import Chunk
from klovis.transforming.markdown_transformer import MarkdownTransformer


def example_markdown_transformer():
    """Exemple : Transformer des chunks en Markdown."""
    print("=" * 60)
    print("📝 MarkdownTransformer - Conversion en Markdown")
    print("=" * 60)
    
    chunks = [
        Chunk(
            text="This is the first chunk with some content.",
            metadata={
                "chunk_id": 0,
                "source": "doc1.txt",
                "title": "Introduction",
            }
        ),
        Chunk(
            text="This is the second chunk with more content.",
            metadata={
                "chunk_id": 1,
                "source": "doc1.txt",
                "title": "Main Content",
            }
        ),
    ]
    
    transformer = MarkdownTransformer(include_metadata=True)
    markdown_chunks = transformer.transform(chunks)
    
    print(f"✅ {len(markdown_chunks)} chunk(s) transformé(s)")
    print(f"\nPremier chunk en Markdown:")
    print(markdown_chunks[0].get('markdown', '')[:200])
    print()


def example_markdown_transformer_without_metadata():
    """Exemple : Transformer sans inclure les métadonnées."""
    print("=" * 60)
    print("📝 MarkdownTransformer - Sans métadonnées")
    print("=" * 60)
    
    chunk = Chunk(
        text="Simple chunk content.",
        metadata={"chunk_id": 0, "source": "doc.txt"}
    )
    
    transformer = MarkdownTransformer(include_metadata=False)
    markdown_chunks = transformer.transform([chunk])
    
    print("Markdown généré (sans métadonnées):")
    print(markdown_chunks[0].get('markdown', ''))
    print()


if __name__ == "__main__":
    print("\n📝 Exemples de Transformers Klovis\n")
    
    example_markdown_transformer()
    example_markdown_transformer_without_metadata()
    
    print("✅ Tous les exemples de transformers ont été exécutés !\n")

