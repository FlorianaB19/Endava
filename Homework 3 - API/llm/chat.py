import re

from openai import OpenAI

from config import OPENAI_API_KEY
from rag.retriever import search_books
from llm.tools import get_summary_by_title

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def build_context(documents: list[str]) -> str:
    """
    Transforms documents received from Chroma into a single context
    """
    return "\n\n".join(documents)


def extract_title(answer: str) -> str | None:
    """
    It tries to extract the recommended title from the GPT response
    """

    possible_titles = [
        "1984",
        "The Hobbit",
        "Harry Potter and the Philosopher's Stone",
        "The Lord of the Rings",
        "Dune",
        "Animal Farm",
        "Brave New World",
        "Fahrenheit 451",
        "The Chronicles of Narnia",
        "The Alchemist",
        "Atomic Habits",
        "Why We Sleep",
        "Dracula",
        "Frankenstein",
        "A Brief History of Time",
        "Pride and Prejudice",
        "The Da Vinci Code"
    ]

    for title in possible_titles:
        if title.lower() in answer.lower():
            return title

    return None


def recommend_book(question: str) -> str:
    """
    Orchestrator RAG + GPT + Summary Tool
    """
    # RAG
    documents = search_books(question) # go in rag/retriever and execute query_embeddings = ....
    context = build_context(documents)

    # GPT recomand a book based on the context and the user question for
    # GPT shouldnt invent books
    system_prompt = """
You are Smart Librarian.

Use ONLY the books from the provided context.

Recommend ONLY ONE book.

Always mention the exact title.

Do NOT invent books. 
"""

    user_prompt = f"""
Context:

{context}

User question:

{question}
"""

    response = client.chat.completions.create(  # the first apel to  GPT 

        model="gpt-4.1-mini",

        temperature=0.3,


        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    recommendation = response.choices[0].message.content #extract the content of the response from GPT

    # Extract title
    title = extract_title(recommendation)

    if not title:
        return recommendation

    # Tool for receive the final book
    summary = get_summary_by_title(title) 

    # GPT builds the final answer
    final_prompt = f"""
The recommended book is:

{title}

Recommendation:

{recommendation}

Detailed summary:

{summary}

Create a friendly answer.

Structure:

1. Recommended Book

2. Why it matches

3. Detailed Summary
"""

    final_response = client.chat.completions.create( # the second apel to GPT for format the final answer

        model="gpt-4.1-mini",

        temperature=0.3,

        messages=[
            {
                "role": "system",
                "content": "You are Smart Librarian."
            },
            {
                "role": "user",
                "content": final_prompt
            }
        ]
    )

    return final_response.choices[0].message.content


if __name__ == "__main__":

    print("=" * 60)
    print("SMART LIBRARIAN")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        question = input("\nQuestion: ")

        if question.lower() == "exit":
            break

        try:

            answer = recommend_book(question)

            print("\n")
            print("=" * 60)
            print(answer)
            print("=" * 60)

        except Exception as e:

            print("\nERROR:")
            print(e)