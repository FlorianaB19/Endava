# 📚 Smart Librarian – AI Book Recommendation System

> **Smart Librarian** is an AI-powered book recommendation system that combines **Retrieval-Augmented Generation (RAG)**, **OpenAI GPT**, **OpenAI Embeddings**, and **ChromaDB** to provide intelligent, context-aware book recommendations.

Unlike a traditional chatbot that relies only on a language model's internal knowledge, Smart Librarian first retrieves the most relevant books from a local vector database using semantic search and then uses GPT to generate a natural recommendation enriched with a detailed book summary.

---

# 🚀 Project Overview

The application follows a **Retrieval-Augmented Generation (RAG)** architecture.

### Workflow

1. The user asks for a book recommendation.
2. The question is converted into an embedding using **OpenAI text-embedding-3-small**.
3. ChromaDB performs semantic search and retrieves the most relevant books.
4. GPT receives only the retrieved books as context.
5. GPT recommends the most suitable book.
6. The backend retrieves the detailed summary from the local JSON knowledge base.
7. GPT generates a conversational response containing:
   - 📖 Recommended Book
   - ✅ Why it matches the user's interests
   - 📚 Detailed Summary

This architecture ensures that recommendations are generated using the local knowledge base instead of relying solely on the model's internal knowledge.

---

# 🏗️ Architecture

```text
                User
                  │
                  ▼
            FastAPI Backend
                  │
                  ▼
          User Question
                  │
                  ▼
       OpenAI Embeddings
                  │
                  ▼
             ChromaDB
                  │
        Top Matching Books
                  ▼
            OpenAI GPT
                  │
                  ▼
      get_summary_by_title()
                  │
                  ▼
      book_summaries.json
                  │
                  ▼
          Final AI Response
```

---

# 🛠️ Technologies Used

- Python 3.14
- FastAPI
- OpenAI API
- GPT-4.1-mini
- OpenAI text-embedding-3-small
- ChromaDB
- Pydantic
- Python-dotenv
- Uvicorn

---

# 📂 Project Structure

```text
smart-librarian/

│
├── api/
│   └── routes.py
│
├── data/
│   ├── book_summaries.txt
│   └── book_summaries.json
│
├── llm/
│   ├── chat.py
│   └── tools.py
│
├── rag/
│   ├── chroma_loader.py
│   ├── embeddings.py
│   └── retriever.py
│
├── utils/
│
├── vector_db/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

---

# 🧠 How RAG Works

Instead of asking GPT directly, the application first retrieves relevant information from a local vector database.

### Step 1

The user asks:

```
I want a book about friendship and magic.
```

### Step 2

The question is transformed into an embedding using:

```
text-embedding-3-small
```

### Step 3

ChromaDB compares the question embedding with the embeddings of all indexed books.

### Step 4

The three most relevant books are retrieved.

Example:

- Harry Potter and the Philosopher's Stone
- The Hobbit
- The Chronicles of Narnia

### Step 5

These retrieved books become the context sent to GPT.

### Step 6

GPT recommends the most appropriate book.

### Step 7

The backend retrieves the detailed summary using:

```
get_summary_by_title()
```

### Step 8

GPT generates the final conversational response.

---

# 🔍 Features

- Semantic search using ChromaDB
- OpenAI Embeddings
- GPT-powered recommendations
- Local book knowledge base
- Detailed book summaries
- REST API with FastAPI
- Interactive Swagger documentation

---

# 🔐 Environment Variables

For security reasons, the OpenAI API key is **not included** in this repository.

Create a file named:

```
.env
```

using the provided template:

```
.env.example
```

Example:

```text
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

The `.env` file is ignored by Git and should never be committed.

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project folder:

```bash
cd smart-librarian
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Build the Vector Database

Whenever `book_summaries.txt` is modified, rebuild the vector database:

```bash
py -m rag.chroma_loader
```

---

# ▶️ Test the Retriever

```bash
py -m rag.retriever
```

---

# ▶️ Run the Chatbot

```bash
py -m llm.chat
```

---

# ▶️ Run the API

```bash
py -m uvicorn app:app --reload
```

Open Swagger:

```
http://127.0.0.1:8000/docs
```

---

# 📚 Example Questions

- I want a fantasy book.
- Recommend a horror novel.
- I love science fiction.
- I want a book about health.
- Recommend a personal development book.
- What is 1984?
- Recommend a romance novel.

---

# 📖 Learning Outcomes

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation (RAG)
- Vector databases
- Semantic Search
- OpenAI Embeddings
- GPT Integration
- REST APIs
- FastAPI
- Backend orchestration
- AI application architecture

---

# 💡 Future Improvements

- Native OpenAI Function Calling
- Text-to-Speech (TTS)
- Speech-to-Text (STT)
- AI Image Generation
- React Frontend
- User Authentication
- Book Rating System

---

# 👨‍💻 Author

Developed as an educational AI project demonstrating the integration of **OpenAI GPT**, **OpenAI Embeddings**, **ChromaDB**, **FastAPI**, and **Retrieval-Augmented Generation (RAG)** to build an intelligent book recommendation system.