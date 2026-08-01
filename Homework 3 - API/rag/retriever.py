from pathlib import Path

import chromadb

from rag.embeddings import create_embedding

# Project Director
BASE_DIR = Path(__file__).resolve().parent.parent

# ChromaDB location
CHROMA_PATH = BASE_DIR / "vector_db"

# Connection to the vector basis
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

collection = client.get_collection("books")


def search_books(query: str, n_results: int = 3):
    """
    Search semantically for the closest books.
    """

    query_embedding = create_embedding(query) #trasnfiorm the book into a vector representation using OpenAI embeddings!!!!!

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0]


if __name__ == "__main__":

    while True:

        question = input("\nQuestion: ")

        if question.lower() == "exit":
            break

        books = search_books(question)

        print("\nRezultate:\n")

        for i, book in enumerate(books, start=1):
            print(f"===== Result {i} =====")
            print(book)
            print()


#Which book is semantically closest to the users question? 

