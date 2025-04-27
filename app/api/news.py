from fastapi import APIRouter
from app.services.fetch_news import fetch_and_store_news, get_articles_for_today, get_all_articles

router = APIRouter()

@router.get("/fetch")
async def fetch_news(category: str = "technology", country: str = "us"):
    """
    Fetch latest news articles and store them in database.
    """
    result = await fetch_and_store_news(category, country)
    return result

@router.get("/get-today")
async def get_today_articles():
    """
    Get today's articles from the database.
    """
    result = await get_articles_for_today()
    return result

@router.get("/get-all")
async def get_all_articles_endpoint():
    """
    Get all available articles.
    """
    result = await get_all_articles()
    return result