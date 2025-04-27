from fastapi import APIRouter
from app.services.chatbot import answer_query

router = APIRouter()

@router.get("/ask")
async def ask_news_chatbot(query: str):
    """
    Ask questions related to current news articles.
    """
    result = await answer_query(query)
    return result
