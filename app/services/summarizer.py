import os
from google import genai
from app.db.mongo import get_collection
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=GEMINI_API_KEY)
client = genai.Client(api_key=GEMINI_API_KEY)

# Choose Gemini model
model = "gemini-2.0-flash"

async def summarize_text(text: str) -> str:
    """
    Use Google Gemini to summarize a given text.
    """
    prompt = f"You are an agent who summarizes text content.\n Make sure to avoid any jargon or overly technical language\n and don't add any template prefix or suffix to the summary, like 'Here is the generated summary' etc\n Summarize the following news article into 3-4 sentences:\n\n{text}"
    try:
        response = client.models.generate_content(model=model, contents=[prompt])
        return response.text.strip()
    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""

async def summarize_all_articles():
    """
    Find all articles without a summary and summarize them.
    """
    articles_collection = await get_collection("articles")
    cursor = articles_collection.find({"summary": None})

    updated_count = 0
    async for article in cursor:
        content = article.get("content") or article.get("description") or article.get("title")
        if not content:
            continue

        summary = await summarize_text(content)

        await articles_collection.update_one(
            {"_id": article["_id"]},
            {"$set": {"summary": summary}}
        )
        updated_count += 1

    return {"message": f"Summarized {updated_count} articles"}
