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
    Performs semantic search and returns relevant books
    together with their ChromaDB distances.
    """

    MAX_DISTANCE = 1.25

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=[
            "documents",
            "distances",
            "metadatas"
        ]
    )

    retrieved_books = []

    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]

    for document, distance, metadata in zip(
        documents,
        distances,
        metadatas
    ):

        # Ignore weak semantic matches
        if distance > MAX_DISTANCE:
            continue

        retrieved_books.append(
            {
                "title": metadata.get(
                    "title",
                    "Unknown"
                ),
                "document": document,
                "distance": round(distance, 4)
            }
        )

    return retrieved_books


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

