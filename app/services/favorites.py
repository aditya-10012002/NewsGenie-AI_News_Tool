from app.db.mongo import get_collection
from bson import ObjectId

async def add_favorite(user_id: str, article_id: str):
    users_collection = await get_collection("users")

    user = await users_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        await users_collection.insert_one({
            "_id": ObjectId(user_id),
            "favorites": [ObjectId(article_id)]
        })
    else:
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"favorites": ObjectId(article_id)}}
        )

    return {"message": "Article added to favorites"}

async def get_favorites(user_id: str):
    users_collection = await get_collection("users")
    articles_collection = await get_collection("articles")

    user = await users_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return {"favorites": []}
    
    favorites_ids = user.get("favorites", [])
    favorites = []
    
    if favorites_ids:
        cursor = articles_collection.find({"_id": {"$in": favorites_ids}})
        async for article in cursor:
            favorites.append({
                "_id": str(article["_id"]),
                "title": article.get("title", ""),
                "summary": article.get("summary", ""),
                "url": article.get("url", "")
            })
    return {"favorites": favorites}

async def remove_favorite(user_id: str, article_id: str):
    users = await get_collection("users")
    result = await users.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"favorites": ObjectId(article_id)}}
    )
    return {"status": "removed"}