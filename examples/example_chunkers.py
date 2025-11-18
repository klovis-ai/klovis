"""
Exemples d'utilisation des différents chunkers de Klovis.

Les chunkers divisent les documents en petits morceaux (chunks)
pour faciliter l'indexation et la recherche sémantique.
"""

from klovis.models import Document, Chunk
from klovis.chunking import SimpleChunker, MarkdownChunker
from klovis.merger import SemanticMerger


def example_simple_chunker():
    """Exemple : Découpage simple par taille."""
    print("=" * 60)
    print("✂️ SimpleChunker - Découpage par taille")
    print("=" * 60)
    
    # Créer un long texte
    long_text = "This is a sentence. " * 100
    doc = Document(source="test.txt", content=long_text)
    
    chunker = SimpleChunker(
        chunk_size=200,  # 200 caractères par chunk
        chunk_overlap=50,  # 50 caractères de chevauchement
        smart_overlap=True,  # Évite de couper au milieu d'un mot
    )
    
    chunks = chunker.chunk([doc])
    
    print(f"✅ Document original: {len(doc.content)} caractères")
    print(f"✅ {len(chunks)} chunk(s) généré(s)")
    print(f"\nPremier chunk ({len(chunks[0].text)} caractères):")
    print(f"  {chunks[0].text[:100]}...")
    print(f"\nMétadonnées du premier chunk:")
    print(f"  {chunks[0].metadata}")
    print()


def example_markdown_chunker():
    """Exemple : Découpage basé sur les titres Markdown."""
    print("=" * 60)
    print("📑 MarkdownChunker - Découpage par titres Markdown")
    print("=" * 60)
    
    markdown_content = """# Introduction

This is the introduction section with some content.

## Section 1.1

Content for section 1.1 goes here.

## Section 1.2

Content for section 1.2 goes here.

# Main Content

This is the main content section.

## Subsection 2.1

Content for subsection 2.1.
"""
    
    doc = Document(source="test.md", content=markdown_content)
    
    chunker = MarkdownChunker(
        max_chunk_size=200,  # Taille max par chunk
        overlap=50,  # Chevauchement entre chunks
    )
    
    chunks = chunker.chunk([doc])
    
    print(f"✅ Document Markdown: {len(doc.content)} caractères")
    print(f"✅ {len(chunks)} chunk(s) généré(s) basés sur les titres")
    print(f"\nPremiers chunks:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n  Chunk {i+1} (type: {chunk.metadata.get('type')}):")
        print(f"  {chunk.text[:80]}...")
    print()


def example_markdown_chunker_with_merger():
    """Exemple : MarkdownChunker avec SemanticMerger."""
    print("=" * 60)
    print("🔗 MarkdownChunker + SemanticMerger")
    print("=" * 60)
    
    # Note: Cet exemple nécessite un embedder réel
    # Pour l'exemple, on montre juste la structure
    
    markdown_content = """# Topic 1
Content about topic 1.

# Topic 2
Content about topic 2.
"""
    
    doc = Document(source="test.md", content=markdown_content)
    
    # Créer un chunker avec merger (nécessite un embedder)
    # embedder = YourEmbedder()  # À remplacer par un vrai embedder
    # merger = SemanticMerger(embedder=embedder, max_size=2000)
    # chunker = MarkdownChunker(max_chunk_size=500, merger=merger)
    
    # Pour l'exemple, on utilise sans merger
    chunker = MarkdownChunker(max_chunk_size=500)
    chunks = chunker.chunk([doc])
    
    print(f"✅ {len(chunks)} chunk(s) généré(s)")
    print("💡 Pour utiliser avec SemanticMerger, passez-le en paramètre:")
    print("   chunker = MarkdownChunker(max_chunk_size=500, merger=merger)")
    print()


if __name__ == "__main__":
    print("\n✂️ Exemples de Chunkers Klovis\n")
    
    example_simple_chunker()
    example_markdown_chunker()
    example_markdown_chunker_with_merger()
    
    print("✅ Tous les exemples de chunkers ont été exécutés !\n")

