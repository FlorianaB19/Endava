from rag.embeddings import create_embedding

embedding = create_embedding("The Hobbit")

print(type(embedding))

print(len(embedding))

print(embedding[:10])



# py -m rag.chroma_loader  si afiseaza ca au fost adaugate 10 carti in ChromaDB 
# py -m rag.retriever si apoi pune o intrebare si iti va returna cele mai apropiate 3 carti din ChromaDB


# for tools.py 

from llm.tools import get_summary_by_title

print(get_summary_by_title("The Hobbit"))

print(get_summary_by_title("1984"))

print(get_summary_by_title("Carte care nu există"))




