from fastapi import APIRouter
from app.services.summarizer import summarize_all_articles

router = APIRouter()

@router.get("/run")
async def summarize_articles():
    """
    Summarize all articles that don't have a summary yet.
    """
    result = await summarize_all_articles()
    return result