"""Chat API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional

from models.chat import ChatRequest, ChatResponse, ChatMessage, ConversationList
from services.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Send a chat message and get AI response."""
    try:
        response = await chat_service.chat(
            message=request.message,
            conversation_id=request.conversation_id,
            user_id=request.user_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}/history", response_model=List[ChatMessage])
async def get_conversation_history(conversation_id: str) -> List[ChatMessage]:
    """Get conversation history."""
    try:
        messages = chat_service.get_conversation_history(conversation_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversations/{conversation_id}")
async def clear_conversation(conversation_id: str) -> dict:
    """Clear conversation memory."""
    try:
        success = chat_service.clear_conversation(conversation_id)
        if success:
            return {"message": "Conversation cleared successfully"}
        else:
            raise HTTPException(status_code=404, detail="Conversation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "chat"}
