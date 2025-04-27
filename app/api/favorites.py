from fastapi import APIRouter
from app.services.favorites import add_favorite, get_favorites, remove_favorite

router = APIRouter()

@router.post("/add")
async def add_to_favorites(user_id: str, article_id: str):
    """
    Add an article to the user's favorites list.
    """
    result = await add_favorite(user_id, article_id)
    return result

@router.get("/get")
async def get_user_favorites(user_id: str):
    """
    Get all favorite articles for a user.
    """
    result = await get_favorites(user_id)
    return result

@router.post("/remove")
async def remove_from_favorites(user_id: str, article_id: str):
    """
    Remove an article from the user's favorites list.
    """
    result = await remove_favorite(user_id, article_id)
    return result
