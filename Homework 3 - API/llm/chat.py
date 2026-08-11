import json

from openai import OpenAI

from config import OPENAI_API_KEY
from rag.retriever import search_books
from llm.tools import TOOLS, get_summary_by_title


# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def build_context(books: list[dict]) -> str:
    """
    Combines the documents retrieved from ChromaDB
    into a single context for GPT.
    """

    return "\n\n".join(
        book["document"]
        for book in books
    )


def recommend_book(question: str) -> dict:
    """
    Smart Librarian orchestration:

    1. Validate input
    2. Retrieve relevant books using RAG
    3. Ask GPT to select one book
    4. GPT requests get_summary_by_title()
    5. Python executes the requested tool
    6. Tool result is returned to GPT
    7. GPT generates the final answer
    """

    # =========================================================
    # 1. INPUT VALIDATION
    # =========================================================

    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "retrieved_books": []
        }

    if question.isdigit():
        return {
            "answer": (
                "Please enter a meaningful question "
                "about books instead of only numbers."
            ),
            "retrieved_books": []
        }

    if len(question) < 3:
        return {
            "answer": "Please enter a more descriptive question.",
            "retrieved_books": []
        }

    # =========================================================
    # 2. RAG RETRIEVAL
    # =========================================================

    books = search_books(
        query=question,
        n_results=3
    )

    if not books:
        return {
            "answer": (
                "Sorry, I couldn't find any relevant book "
                "for your request in the current library."
            ),
            "retrieved_books": []
        }

    context = build_context(books)

    # =========================================================
    # 3. FIRST GPT CALL
    # =========================================================

    system_prompt = """
You are Smart Librarian, an AI book recommendation assistant.

You receive books retrieved from a local ChromaDB vector database.

Rules:

1. Use ONLY books from the provided context.
2. Select exactly ONE book that best matches the user's request.
3. Do NOT invent books.
4. Do NOT invent summaries.
5. After selecting the book, call get_summary_by_title.
6. Pass the EXACT book title to the tool.
7. The detailed summary must come from the tool.
"""

    user_prompt = f"""
Retrieved books:

{context}

User question:

{question}

Select the most appropriate book and retrieve its detailed summary.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.3,
        messages=messages,
        tools=TOOLS,
        tool_choice={
            "type": "function",
            "function": {
                "name": "get_summary_by_title"
            }
        }
    )

    assistant_message = response.choices[0].message

    # The assistant message contains the tool request.
    messages.append(assistant_message)

    # =========================================================
    # 4. CHECK TOOL CALL
    # =========================================================

    if not assistant_message.tool_calls:

        return {
            "answer": (
                assistant_message.content
                or "No recommendation was generated."
            ),
            "retrieved_books": books
        }

    selected_title = None

    # =========================================================
    # 5. EXECUTE TOOL
    # =========================================================

    for tool_call in assistant_message.tool_calls:

        if tool_call.function.name == "get_summary_by_title":

            arguments = json.loads(
                tool_call.function.arguments
            )

            selected_title = arguments["title"]

            # Temporary debug messages.
            print("\n" + "=" * 60)
            print("NATIVE FUNCTION CALLING")
            print("=" * 60)

            print(
                "Tool requested:",
                tool_call.function.name
            )

            print(
                "Book title:",
                selected_title
            )

            # Execute our LOCAL Python function.
            summary = get_summary_by_title(
                selected_title
            )

            print(
                "Tool executed successfully."
            )

            print(
                "Summary returned by tool:"
            )

            print(summary)

            print("=" * 60 + "\n")

            # Return the tool result to GPT.
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": summary
                }
            )

    # =========================================================
    # 6. FINAL INSTRUCTIONS FOR GPT
    # =========================================================

    messages.append(
        {
            "role": "system",
            "content": """
The tool has now returned the verified detailed summary.

Generate the final Smart Librarian response.

You MUST use this exact structure:

### 1. Recommended Book

Mention the exact book title and author.

### 2. Why It Matches

Explain briefly why this book matches the user's request,
using the retrieved context.

### 3. Detailed Summary

Present the detailed summary returned by
get_summary_by_title.

Do not ask the user whether they want more information.

Do not invent information that was not present
in the retrieved context or tool result.
"""
        }
    )

    # =========================================================
    # 7. SECOND GPT CALL
    # =========================================================

    final_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.3,
        messages=messages
    )

    answer = (
        final_response
        .choices[0]
        .message
        .content
    )

    if not answer:
        answer = (
            "The recommendation was generated, "
            "but the final response was empty."
        )

    # =========================================================
    # 8. RETURN TO FASTAPI
    # =========================================================

    return {
        "answer": answer,
        "retrieved_books": books
    }


# =============================================================
# CLI TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SMART LIBRARIAN")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        question = input("\nQuestion: ").strip()

        if question.lower() == "exit":
            break

        try:

            result = recommend_book(question)

            print("\n")
            print("=" * 60)

            # IMPORTANT:
            # Print only the final answer,
            # not the entire dictionary.
            print(result["answer"])

            print("=" * 60)

        except Exception as error:

            print("\nERROR:")
            print(error)