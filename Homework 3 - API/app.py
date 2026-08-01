from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="Smart Librarian API",
    description="Book recommendation system using OpenAI GPT + RAG + ChromaDB",
    version="1.0.0"
)

app.include_router(router)

# graphic interface for the site 
# FastAPI also automatically generates the file /openai.json
