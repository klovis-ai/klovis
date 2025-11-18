"""
Exemples d'utilisation des différents cleaners de Klovis.

Les cleaners permettent de nettoyer et normaliser le texte des documents
avant le chunking et l'indexation.
"""

from klovis.models import Document
from klovis.cleaning import (
    HTMLCleaner,
    TextCleaner,
    NormalizeCleaner,
    EmojiCleaner,
    CompositeCleaner,
)


def example_html_cleaner():
    """Exemple : Nettoyer le HTML d'un document."""
    print("=" * 60)
    print("🧹 HTMLCleaner - Nettoyage du HTML")
    print("=" * 60)
    
    dirty_html = """
    <html>
        <head><title>Test</title></head>
        <body>
            <h1>Hello World</h1>
            <p>This is a <strong>test</strong> paragraph.</p>
            <script>alert('bad');</script>
        </body>
    </html>
    """
    
    doc = Document(source="test.html", content=dirty_html)
    cleaner = HTMLCleaner()
    cleaned = cleaner.clean([doc])
    
    print("Avant:")
    print(dirty_html[:100])
    print("\nAprès:")
    print(cleaned[0].content[:100])
    print()


def example_text_cleaner():
    """Exemple : Nettoyer le texte (espaces, caractères spéciaux)."""
    print("=" * 60)
    print("📝 TextCleaner - Nettoyage du texte")
    print("=" * 60)
    
    dirty_text = """
    This   is    a    text    with    multiple    spaces.
    
    And some special characters: @#$%^&*()
    """
    
    doc = Document(source="test.txt", content=dirty_text)
    cleaner = TextCleaner()
    cleaned = cleaner.clean([doc])
    
    print("Avant:")
    print(repr(dirty_text))
    print("\nAprès:")
    print(repr(cleaned[0].content))
    print()


def example_normalize_cleaner():
    """Exemple : Normaliser le texte (lowercase, unicode)."""
    print("=" * 60)
    print("🔤 NormalizeCleaner - Normalisation du texte")
    print("=" * 60)
    
    text = "HELLO World! This is a TÉST with émojis 🎉"
    
    doc = Document(source="test.txt", content=text)
    
    # Avec lowercase
    cleaner = NormalizeCleaner(lowercase=True, preserve_newlines=True)
    cleaned = cleaner.clean([doc])
    
    print("Avant:")
    print(text)
    print("\nAprès (lowercase):")
    print(cleaned[0].content)
    print()


def example_emoji_cleaner():
    """Exemple : Gérer les emojis."""
    print("=" * 60)
    print("😀 EmojiCleaner - Gestion des emojis")
    print("=" * 60)
    
    text = "Hello! 🎉 This is great! 🚀 Let's go! 💪"
    
    doc = Document(source="test.txt", content=text)
    
    # Supprimer les emojis
    cleaner = EmojiCleaner(replace=False)
    cleaned = cleaner.clean([doc])
    
    print("Avant:")
    print(text)
    print("\nAprès (emojis supprimés):")
    print(cleaned[0].content)
    print()


def example_composite_cleaner():
    """Exemple : Utiliser plusieurs cleaners en séquence."""
    print("=" * 60)
    print("🔗 CompositeCleaner - Pipeline de nettoyage")
    print("=" * 60)
    
    dirty_text = """
    <html>
        <body>
            <h1>HELLO   WORLD!   🎉</h1>
            <p>This   is   a   test   with   multiple   spaces.</p>
        </body>
    </html>
    """
    
    doc = Document(source="test.html", content=dirty_text)
    
    # Pipeline de nettoyage : HTML -> Text -> Normalize -> Emoji
    pipeline = CompositeCleaner([
        HTMLCleaner(),
        TextCleaner(),
        NormalizeCleaner(lowercase=True, preserve_newlines=True),
        EmojiCleaner(replace=False),
    ])
    
    cleaned = pipeline.clean([doc])
    
    print("Avant:")
    print(dirty_text)
    print("\nAprès (pipeline complet):")
    print(cleaned[0].content)
    print()


if __name__ == "__main__":
    print("\n🧹 Exemples de Cleaners Klovis\n")
    
    example_html_cleaner()
    example_text_cleaner()
    example_normalize_cleaner()
    example_emoji_cleaner()
    example_composite_cleaner()
    
    print("✅ Tous les exemples de cleaners ont été exécutés !\n")

