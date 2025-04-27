import os
import httpx
from app.db.mongo import get_collection
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

async def fetch_and_store_news(category: str, country: str):
    params = {
        "category": category,
        "country": country,
        "apiKey": NEWS_API_KEY,
        "pageSize": 20
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(NEWS_API_URL, params=params)
        data = response.json()

    if data["status"] != "ok":
        return {"error": "Failed to fetch news"}

    articles = data["articles"]
    news_collection = await get_collection("articles")

    stored_articles = []
    for article in articles:
        article_doc = {
            "title": article.get("title"),
            "description": article.get("description"),
            "content": article.get("content"),
            "url": article.get("url"),
            "publishedAt": article.get("publishedAt", datetime.utcnow().isoformat()),
            "source": article.get("source", {}).get("name"),
            "category": category,
            "country": country,
            "summary": None,  # Placeholder for summarized content
            "embedding": None  # Placeholder for future embeddings
        }
        await news_collection.insert_one(article_doc)
        stored_articles.append(article_doc)

    return {"message": f"Stored {len(stored_articles)} articles"}


async def get_articles_for_today():
    collection = await get_collection("articles")
    today = datetime.utcnow().date()  # e.g., 2025-04-27

    # Define start and end of today (UTC)
    start_of_day = datetime(today.year, today.month, today.day)
    end_of_day = start_of_day + timedelta(days=1)

    cursor = collection.find({
        "publishedAt": {
            "$gte": start_of_day.isoformat() + "Z",  # "2025-04-27T00:00:00Z"
            "$lt": end_of_day.isoformat() + "Z"       # "2025-04-28T00:00:00Z"
        }
    }).sort("publishedAt", -1)

    articles = []
    async for article in cursor:
        articles.append({
            "_id": str(article["_id"]),
            "title": article.get("title", ""),
            "summary": article.get("summary", ""),
            "url": article.get("url", "")
        })
    return {"articles": articles}

async def get_all_articles():
    collection = await get_collection("articles")
    cursor = collection.find({}).sort("publishedAt", -1)

    articles = []
    async for article in cursor:
        articles.append({
            "_id": str(article["_id"]),
            "title": article.get("title", ""),
            "summary": article.get("summary", ""),
            "url": article.get("url", "")
        })
    return {"articles": articles}