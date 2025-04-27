import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.db.mongo import get_collection
from bson import ObjectId

# Load sentence transformer model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Global FAISS index (for now, kept simple)
index = faiss.IndexFlatL2(384)  # 384 is the dimension for 'MiniLM-L6-v2'
article_ids = []  # To map FAISS index to MongoDB articles

async def generate_embeddings():
    articles_collection = await get_collection("articles")
    cursor = articles_collection.find({"embedding": None, "summary": {"$ne": None}})

    new_embeddings = []
    ids = []

    async for article in cursor:
        summary = article.get("summary")
        if not summary:
            continue

        embedding = embedding_model.encode(summary)
        new_embeddings.append(embedding)
        ids.append(str(article["_id"]))

        await articles_collection.update_one(
            {"_id": article["_id"]},
            {"$set": {"embedding": embedding.tolist()}}
        )

    if new_embeddings:
        vectors = np.array(new_embeddings).astype(np.float32)
        index.add(vectors)
        article_ids.extend(ids)

    return {"message": f"Generated embeddings for {len(new_embeddings)} articles"}

async def recommend_articles(article_id: str):
    articles_collection = await get_collection("articles")
    article = await articles_collection.find_one({"_id": ObjectId(article_id)})

    if not article or not article.get("embedding"):
        return {"error": "Article not found or not embedded"}

    query_vector = np.array(article["embedding"]).astype(np.float32).reshape(1, -1)
    D, I = index.search(query_vector, k=5)  # Get top-5 similar articles

    recommended = []
    for idx in I[0]:
        if idx < len(article_ids):
            rec_id = article_ids[idx]
            rec_article = await articles_collection.find_one({"_id": ObjectId(rec_id)})
            if rec_article:
                recommended.append({
                    "title": rec_article.get("title"),
                    "summary": rec_article.get("summary"),
                    "url": rec_article.get("url")
                })

    return {"recommended_articles": recommended}
