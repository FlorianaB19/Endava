# 📚 Smart Librarian – AI Book Recommendation System

> **Smart Librarian** is an AI-powered, multimodal book recommendation system built with **Retrieval-Augmented Generation (RAG)**, **OpenAI GPT**, **OpenAI Embeddings**, **ChromaDB**, **FastAPI**, and **Streamlit**.

Unlike a traditional chatbot that relies only on a language model's internal knowledge, Smart Librarian searches a local book knowledge base using semantic vector search before generating a recommendation.

The application also supports **voice input**, **spoken AI responses**, **native OpenAI function calling**, **RAG explainability**, and **user feedback**.

---

# 🚀 Project Overview

Smart Librarian combines semantic search, generative AI, tool calling, voice technologies, and a REST API into a complete AI application.

A user can type or speak a request such as:

```text
I want a book about friendship and magic.
```

The system searches the local vector database, identifies relevant books, asks GPT to select the best recommendation, retrieves a verified detailed summary using a local tool, and generates a conversational response.

The final recommendation can also be played as audio using Text-to-Speech.

---

# ✨ Main Features

- 🔍 **Retrieval-Augmented Generation (RAG)**
- 🧠 **OpenAI Embeddings**
- 📚 **ChromaDB vector database**
- 🤖 **GPT-powered recommendations**
- 🛠️ **Native OpenAI Function Calling**
- 📖 **Local verified book summaries**
- 🎤 **Speech-to-Text voice input**
- 🔊 **Text-to-Speech responses**
- 🔎 **RAG Explainability panel**
- 👍 **User feedback system**
- ⚡ **FastAPI REST backend**
- 💻 **Streamlit chat interface**
- 📑 **Swagger API documentation**
- 🛡️ **Input validation and relevance filtering**

---

# 🏗️ Architecture

```text
                         USER
                          │
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
             ⌨️ Text           🎤 Voice
                                   │
                                   ▼
                            Speech-to-Text
                                   │
                 └────────┬────────┘
                          │
                          ▼
                      Streamlit
                          │
                          │ HTTP POST /chat
                          ▼
                       FastAPI
                          │
                          ▼
                   Input Validation
                          │
                          ▼
                   OpenAI Embedding
                          │
                          ▼
                      ChromaDB
                          │
                  Semantic Retrieval
                          │
                          ▼
                 Relevant Book Context
                          │
                          ▼
                     OpenAI GPT
                          │
                          ▼
                  Native Tool Call
                          │
                          ▼
              get_summary_by_title()
                          │
                          ▼
                book_summaries.json
                          │
                          ▼
                     OpenAI GPT
                          │
                          ▼
                   Final Response
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          💬 Text       🔊 Audio     👍 Feedback
                          │
                          ▼
                    Text-to-Speech
```

---

# 🧠 How RAG Works

**Retrieval-Augmented Generation (RAG)** allows the language model to generate responses using information retrieved from an external knowledge base.

Instead of asking GPT directly for a recommendation, Smart Librarian first searches its own collection of books.

## Step 1 — User Query

The user asks:

```text
I want a book about friendship and magic.
```

The question can be typed or recorded using the microphone.

---

## Step 2 — Embedding Generation

The question is transformed into a numerical vector using:

```text
text-embedding-3-small
```

Conceptually:

```text
"I want a book about friendship and magic"

                ↓

[0.021, -0.183, 0.442, ...]
```

The vector represents the semantic meaning of the text.

---

## Step 3 — Vector Search

ChromaDB stores embeddings for all indexed books.

The query embedding is compared with the stored book embeddings.

The system retrieves the books with the smallest vector distances.

Example:

```text
1. Harry Potter and the Philosopher's Stone
2. The Chronicles of Narnia
3. The Hobbit
```

A smaller vector distance indicates a stronger semantic match.

---

## Step 4 — Relevance Filtering

Retrieving the closest document does not automatically mean that the document is relevant.

For this reason, Smart Librarian applies a distance threshold.

Weak semantic matches are rejected before reaching GPT.

This prevents meaningless inputs such as:

```text
asdfghjkl
```

from generating unrelated book recommendations.

---

## Step 5 — GPT Recommendation

The retrieved books become the context provided to GPT.

GPT is instructed to:

- use only books from the retrieved context;
- recommend exactly one book;
- never invent books;
- retrieve the detailed summary through the available tool.

This reduces hallucination and keeps recommendations grounded in the local knowledge base.

---

# 🛠️ Native OpenAI Function Calling

After selecting the best book, GPT requests the local function:

```python
get_summary_by_title(title)
```

For example:

```text
GPT selects:
Harry Potter and the Philosopher's Stone

            ↓

Tool Call:
get_summary_by_title(
    "Harry Potter and the Philosopher's Stone"
)

            ↓

book_summaries.json

            ↓

Verified detailed summary
```

The backend executes the requested Python function and sends the result back to GPT.

GPT then generates the final response using the verified summary.

The final answer follows the structure:

```text
1. Recommended Book

2. Why It Matches

3. Detailed Summary
```

This separates **LLM reasoning** from **trusted local data retrieval**.

---

# 🔍 RAG Explainability

Smart Librarian includes an explainability panel in the Streamlit interface.

Users can expand:

```text
🔍 How was this recommendation found?
```

to inspect the books retrieved from ChromaDB.

Example:

```text
Retrieved Books

1. Harry Potter and the Philosopher's Stone
   Vector distance: 1.1145

2. The Chronicles of Narnia
   Vector distance: 1.1685

3. The Hobbit
   Vector distance: 1.1759
```

This makes the retrieval process visible instead of treating the AI recommendation as a black box.

> Lower vector distance indicates a stronger semantic match.

---

# 🎤 Speech-to-Text

Users can interact with Smart Librarian using their microphone.

Example spoken request:

```text
Recommend me a science fiction book.
```

The audio is converted into text before entering the normal RAG pipeline.

```text
Microphone
    │
    ▼
Speech-to-Text
    │
    ▼
User Question
    │
    ▼
RAG Pipeline
```

The rest of the application does not need to know whether the question originally came from the keyboard or from voice input.

---

# 🔊 Text-to-Speech

AI recommendations can also be converted into speech.

After receiving a recommendation, the user can select:

```text
🔊 Listen
```

The generated response is converted into audio and played directly inside the Streamlit interface.

This provides a complete multimodal interaction:

```text
Voice → Text → RAG → GPT → Text → Voice
```

---

# 👍 User Feedback

Each recommendation includes:

```text
Was this recommendation useful?

👍 Yes        👎 No
```

Feedback is stored locally in:

```text
data/feedback.jsonl
```

Each record contains information such as:

```json
{
  "timestamp": "2026-08-11T18:30:00",
  "question": "I want a fantasy book.",
  "answer": "I recommend...",
  "rating": "positive"
}
```

JSON Lines (`.jsonl`) allows new feedback entries to be appended without rewriting the entire file.

This provides a simple foundation for evaluating recommendation quality.

---

# ⚡ FastAPI Backend

FastAPI exposes the recommendation system through a REST API.

The main endpoint is:

```text
POST /chat
```

Example request:

```json
{
  "question": "I want a fantasy book."
}
```

Example response:

```json
{
  "answer": "I recommend...",
  "retrieved_books": [
    {
      "title": "The Hobbit",
      "document": "...",
      "distance": 1.15
    }
  ]
}
```

FastAPI also automatically generates interactive Swagger documentation.

---

# 💻 Streamlit Frontend

Streamlit provides the graphical chat interface.

The frontend supports:

- typed questions;
- microphone recording;
- conversation history;
- RAG explainability;
- audio playback;
- user feedback;
- error handling;
- example prompts.

Streamlit communicates with FastAPI through HTTP requests instead of directly calling the recommendation functions.

This keeps the frontend and backend separated.

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Main programming language |
| **OpenAI GPT** | Recommendation reasoning and response generation |
| **OpenAI Embeddings** | Semantic vector representation |
| **ChromaDB** | Vector database and semantic retrieval |
| **FastAPI** | REST API backend |
| **Streamlit** | Interactive frontend |
| **OpenAI Function Calling** | Local tool orchestration |
| **Speech-to-Text** | Voice input transcription |
| **Text-to-Speech** | Spoken AI responses |
| **Pydantic** | API request/response validation |
| **python-dotenv** | Environment variable management |
| **Uvicorn** | ASGI web server |
| **Requests** | Streamlit → FastAPI HTTP communication |

---

# 📂 Project Structure

```text
Homework 3 - API/
│
├── api/
│   └── routes.py
│
├── data/
│   ├── book_summaries.txt
│   ├── book_summaries.json
│   └── feedback.jsonl
│
├── llm/
│   ├── audio.py
│   ├── chat.py
│   └── tools.py
│
├── rag/
│   ├── chroma_loader.py
│   ├── embeddings.py
│   └── retriever.py
│
├── utils/
│   └── feedback.py
│
├── vector_db/
│
├── app.py
├── config.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

> `.env` is intentionally excluded from the repository because it contains the private OpenAI API key.

---

# 📚 Local Knowledge Base

Smart Librarian uses two main book data sources.

## `book_summaries.txt`

Used for:

```text
Semantic Search → Embeddings → ChromaDB
```

It contains information such as:

- title;
- author;
- genre;
- summary;
- themes;
- keywords.

---

## `book_summaries.json`

Used by:

```python
get_summary_by_title()
```

It provides the verified detailed summary for an exact title.

This creates a useful separation:

```text
book_summaries.txt
        ↓
Semantic Retrieval

book_summaries.json
        ↓
Exact Summary Lookup
```

---

# 🔐 Environment Variables

The OpenAI API key is **never stored directly in the source code**.

Create:

```text
.env
```

inside the project directory.

Use:

```env
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

An example configuration is provided in:

```text
.env.example
```

The real `.env` file must remain in `.gitignore`.

**Never commit API keys to GitHub.**

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the API project:

```bash
cd "Endava/Homework 3 - API"
```

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

Create the `.env` file and add your OpenAI API key.

---

# 🗄️ Build the Vector Database

Whenever the book collection in:

```text
data/book_summaries.txt
```

is changed, rebuild ChromaDB:

```bash
py -m rag.chroma_loader
```

The loader:

1. reads the book collection;
2. generates embeddings;
3. recreates the ChromaDB collection;
4. stores the documents, vectors, IDs, and metadata.

---

# 🔍 Test the Retriever

Run:

```bash
py -m rag.retriever
```

Example:

```text
Question: I want a fantasy book.
```

The retriever performs semantic search and returns relevant books that pass the configured distance threshold.

---

# 🤖 Test the Chatbot

Run:

```bash
py -m llm.chat
```

Example:

```text
Question: I want a book about friendship and magic.
```

During development, the CLI can also be used to verify the Native Function Calling workflow.

---

# ⚡ Run FastAPI

Start the backend:

```bash
py -m uvicorn app:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 💻 Run Streamlit

Open a second terminal and run:

```bash
py -m streamlit run streamlit_app.py
```

The interface is normally available at:

```text
http://localhost:8501
```

Both **FastAPI and Streamlit must be running** for the complete application to work.

---

# ▶️ Running the Complete Application

Use two terminals.

### Terminal 1 — Backend

```bash
py -m uvicorn app:app --reload
```

### Terminal 2 — Frontend

```bash
py -m streamlit run streamlit_app.py
```

Then open:

```text
http://localhost:8501
```

---

# 🧪 Example Questions

Try:

```text
I want a fantasy book.
```

```text
I want a book about friendship and magic.
```

```text
Recommend a horror novel.
```

```text
I want a book about health.
```

```text
Recommend a personal development book.
```

```text
I am interested in science fiction.
```

```text
What is 1984 about?
```

```text
Recommend a romance novel.
```

---

# 🛡️ Input Validation

The application also handles invalid or irrelevant requests.

For example:

```text
1234
```

is rejected before unnecessary AI processing.

Queries that do not have a sufficiently relevant match in ChromaDB are also rejected:

```text
asdfghjkl
```

Example response:

```text
Sorry, I couldn't find any relevant book for your request in the current library.
```

This prevents ChromaDB's nearest-neighbor search from forcing an unrelated recommendation.

---

# 🔄 Complete Application Flow

```text
User
 │
 ├───────────────┐
 │               │
 ▼               ▼
Text          Microphone
                 │
                 ▼
          Speech-to-Text
                 │
 └───────┬───────┘
         ▼
     Streamlit
         │
         ▼
   POST /chat
         │
         ▼
     FastAPI
         │
         ▼
 Input Validation
         │
         ▼
OpenAI Embedding
         │
         ▼
     ChromaDB
         │
         ▼
Distance Filtering
         │
         ▼
Retrieved Context
         │
         ▼
        GPT
         │
         ▼
 Native Function Call
         │
         ▼
get_summary_by_title()
         │
         ▼
Verified Local Summary
         │
         ▼
        GPT
         │
         ▼
 Final Recommendation
         │
 ┌───────┼────────────┐
 ▼       ▼            ▼
Text   Audio       Feedback
        │
        ▼
Text-to-Speech
```

---

# 📖 Learning Outcomes

This project demonstrates practical knowledge of:

- Retrieval-Augmented Generation (RAG)
- Large Language Model integration
- Semantic Search
- Vector Embeddings
- Vector Databases
- Prompt Engineering
- Native LLM Function Calling
- Tool Execution
- AI Grounding
- Relevance Filtering
- RAG Explainability
- Speech-to-Text
- Text-to-Speech
- REST API Development
- FastAPI
- Streamlit
- Pydantic Validation
- Frontend/Backend Communication
- User Feedback Collection
- AI Application Architecture

---

# 💡 Future Improvements

Possible future extensions include:

- 🧠 Conversational memory
- 🎨 AI-generated thematic book illustrations
- 👤 User accounts and authentication
- ❤️ Personalized reading profiles
- ⭐ Book ratings and favorites
- 📊 Recommendation analytics dashboard
- 📈 Feedback analysis
- 🔎 Advanced metadata filters
- 📚 Larger external book datasets
- 🐳 Docker deployment
- ☁️ Cloud deployment
- 🧪 Automated RAG evaluation
- 🔄 Streaming GPT responses

---

# 🎯 Key Idea

The main idea behind Smart Librarian is simple:

> **Retrieve first, generate second.**

Instead of allowing the language model to answer exclusively from its internal knowledge, the application first retrieves relevant information from a controlled local knowledge base.

This makes the system more grounded, explainable, and easier to extend.

---

# 👨‍💻 Author

Smart Librarian was developed as an educational AI project demonstrating how modern AI components can be combined into a complete application.

The project integrates:

**OpenAI GPT + OpenAI Embeddings + RAG + ChromaDB + Native Function Calling + FastAPI + Streamlit + Speech-to-Text + Text-to-Speech + Explainability + User Feedback**

to create an intelligent, multimodal, and explainable book recommendation assistant.