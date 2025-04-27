from fastapi import APIRouter
from app.services.recommender import generate_embeddings, recommend_articles

router = APIRouter()

@router.get("/embed")
async def embed_articles():
    """
    Generate embeddings for all summarized articles.
    """
    result = await generate_embeddings()
    return result

@router.get("/get")
async def get_recommendations(article_id: str):
    """
    Get recommended articles similar to the given article ID.
    """
    result = await recommend_articles(article_id)
    return result
