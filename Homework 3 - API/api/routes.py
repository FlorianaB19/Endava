from fastapi import APIRouter
from pydantic import BaseModel

from llm.chat import recommend_book


router = APIRouter()


class ChatRequest(BaseModel):
    question: str


class RetrievedBook(BaseModel):
    title: str
    document: str
    distance: float


class ChatResponse(BaseModel):
    answer: str
    retrieved_books: list[RetrievedBook]


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    result = recommend_book(
        request.question
    )

    return ChatResponse(
        answer=result["answer"],
        retrieved_books=result[
            "retrieved_books"
        ]
    )