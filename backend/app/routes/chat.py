from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.llm_service import get_answer

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    answer = get_answer(chat_request.question)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return {"response": answer}
