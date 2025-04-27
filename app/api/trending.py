from fastapi import APIRouter
from app.services.trending import detect_trending_topics

router = APIRouter()

@router.get("/detect")
async def detect_trending():
    """
    Detect trending keywords from today's articles.
    """
    result = await detect_trending_topics()
    return result