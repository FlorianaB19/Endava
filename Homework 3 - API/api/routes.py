from fastapi import APIRouter
from pydantic import BaseModel

from llm.chat import recommend_book

router = APIRouter()


class ChatRequest(BaseModel):  # bcs we want to receive a json 
    question: str


class ChatResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=ChatResponse) # creates an HTTP POST endpoint, available at /chat
def chat(request: ChatRequest):
    """
    Receives the users question and returns the recommendation
    """

    answer = recommend_book(request.question) # ednpoint receives the question 

    return ChatResponse(answer=answer)