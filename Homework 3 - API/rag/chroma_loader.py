import re
from pathlib import Path

import chromadb

from rag.embeddings import create_embedding

# The project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# The book file
BOOKS_FILE = BASE_DIR / "data" / "book_summaries.txt"

# The ChromaDB file
CHROMA_PATH = BASE_DIR / "vector_db"


def load_books():
    """
    Reads all books from the file.
    """

    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    books = [
        section.strip()
        for section in content.split("--------------------------------------------------")
        if section.strip()
    ]

    return books


def extract_title(book: str) -> str:
    """
    Extracts the title from the book text
    """
    match = re.search(r"## Title:\s*(.+)", book)

    if not match:
        raise ValueError("Title not found.")

    return match.group(1).strip()


def normalize_id(title: str) -> str:
    """
   transform the title into a normalized id for ChromaDB
    """

    return (
        title.lower()
        .replace(" ", "_")
        .replace("'", "")
        .replace(",", "")
        .replace(".", "")
        .replace(":", "")
    )


def build_vector_store():

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    # if exists, delete the old collection
    try:
        client.delete_collection("books")
        print("The old collection has been deleted.")
    except Exception:
        print("No previous collection found.")

    collection = client.create_collection("books")

    books = load_books()

    print(f"\nAu fost găsite {len(books)} cărți.\n")

    for book in books:

        title = extract_title(book)

        book_id = normalize_id(title)

        embedding = create_embedding(book) #trasnfiorm the book into a vector representation using OpenAI embeddings!!!!!

        collection.add(
            ids=[book_id],
            documents=[book],
            embeddings=[embedding],
            metadatas=[{"title": title}] # here i save the title as metadata and documentation
        )

        print(f"✓ {title}")

    print("\nVector Store creat cu succes!")


if __name__ == "__main__":
    build_vector_store()