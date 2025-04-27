from app.db.mongo import get_collection
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

async def detect_trending_topics(top_n=5, articles_per_topic=2):
    articles_collection = await get_collection("articles")
    cursor = articles_collection.find({"summary": {"$ne": None}})
    
    summaries = []
    article_list = []

    async for article in cursor:
        summaries.append(article.get("summary", ""))
        article_list.append(article)

    if not summaries:
        return {"trending_topics": []}

    # TF-IDF Extraction
    tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = tfidf.fit_transform(summaries)
    
    scores = np.sum(tfidf_matrix.toarray(), axis=0)
    terms = tfidf.get_feature_names_out()

    # Get Top-N trending keywords
    top_indices = scores.argsort()[-top_n:][::-1]
    top_keywords = [terms[i] for i in top_indices]

    # Find sample articles matching each keyword
    trending_data = []

    for keyword in top_keywords:
        related_articles = []
        for article in article_list:
            title = article.get("title", "")
            summary = article.get("summary", "")

            # Search keyword in title or summary (case insensitive)
            if re.search(r'\b' + re.escape(keyword) + r'\b', title, re.IGNORECASE) or \
               re.search(r'\b' + re.escape(keyword) + r'\b', summary, re.IGNORECASE):
                related_articles.append({
                    "title": title,
                    "url": article.get("url")
                })

            if len(related_articles) >= articles_per_topic:
                break

        trending_data.append({
            "keyword": keyword,
            "articles": related_articles
        })

    return {"trending_topics": trending_data}
