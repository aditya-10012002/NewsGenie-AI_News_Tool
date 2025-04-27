from fastapi import APIRouter
from app.services.custom_summary import summarize_in_style

router = APIRouter()

@router.post("/summarize-style")
async def summarize_article(article_id: str, style: str):
    """
    Summarize an article in a specific style.
    Available styles: formal, funny, short
    """
    result = await summarize_in_style(article_id, style)
    return result