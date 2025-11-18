"""
Exemples d'utilisation des différents loaders de Klovis.

Les loaders permettent de charger des documents depuis différentes sources
et de les convertir en objets Document.
"""

from pathlib import Path
from klovis.loaders import (
    DirectoryLoader,
    TextFileLoader,
    HTMLLoader,
    JSONLoader,
    PDFLoader,
)
from klovis.models import Document


def example_directory_loader():
    """Exemple : Charger tous les fichiers d'un répertoire."""
    print("=" * 60)
    print("📁 DirectoryLoader - Chargement récursif d'un répertoire")
    print("=" * 60)
    
    loader = DirectoryLoader(
        path="data/",
        recursive=True,  # Parcourt les sous-dossiers
        ignore_hidden=True,  # Ignore les fichiers cachés
        markdownify=True,  # Convertit HTML/PDF en Markdown
    )
    
    documents = loader.load()
    print(f"✅ {len(documents)} document(s) chargé(s)")
    
    for doc in documents[:3]:  # Afficher les 3 premiers
        print(f"  - {doc.source}: {len(doc.content)} caractères")
    print()


def example_text_file_loader():
    """Exemple : Charger un fichier texte simple."""
    print("=" * 60)
    print("📄 TextFileLoader - Chargement d'un fichier texte")
    print("=" * 60)
    
    loader = TextFileLoader("example.txt")
    documents = loader.load(["example.txt"])
    
    if documents:
        doc = documents[0]
        print(f"✅ Fichier chargé: {doc.source}")
        print(f"   Contenu (premiers 100 caractères): {doc.content[:100]}...")
    print()


def example_html_loader():
    """Exemple : Charger un fichier HTML avec conversion Markdown."""
    print("=" * 60)
    print("🌐 HTMLLoader - Chargement et conversion HTML")
    print("=" * 60)
    
    # Chargement avec conversion Markdown
    loader = HTMLLoader(path="example.html", markdownify=True)
    documents = loader.load()
    
    if documents:
        doc = documents[0]
        print(f"✅ HTML chargé: {doc.source}")
        print(f"   Format: {doc.metadata.get('format')}")
        print(f"   Contenu (premiers 150 caractères):")
        print(f"   {doc.content[:150]}...")
    print()


def example_json_loader():
    """Exemple : Charger des données depuis un fichier JSON."""
    print("=" * 60)
    print("📋 JSONLoader - Chargement depuis JSON")
    print("=" * 60)
    
    # Charger depuis un JSON avec un champ personnalisé
    loader = JSONLoader(path="data.json", text_field="content")
    documents = loader.load()
    
    if documents:
        print(f"✅ {len(documents)} document(s) chargé(s) depuis JSON")
        for doc in documents:
            print(f"  - {doc.source}: {len(doc.content)} caractères")
    print()


def example_pdf_loader():
    """Exemple : Charger un fichier PDF."""
    print("=" * 60)
    print("📕 PDFLoader - Chargement d'un PDF")
    print("=" * 60)
    
    loader = PDFLoader(path="document.pdf")
    documents = loader.load()
    
    if documents:
        doc = documents[0]
        print(f"✅ PDF chargé: {doc.source}")
        print(f"   Pages: {doc.metadata.get('pages', 'N/A')}")
        print(f"   Contenu (premiers 200 caractères):")
        print(f"   {doc.content[:200]}...")
    print()


if __name__ == "__main__":
    print("\n🚀 Exemples de Loaders Klovis\n")
    
    # Décommenter l'exemple que vous voulez tester
    # example_directory_loader()
    # example_text_file_loader()
    # example_html_loader()
    # example_json_loader()
    # example_pdf_loader()
    
    print("💡 Décommentez les exemples dans le code pour les tester !\n")

