import os
from google import genai
from app.db.mongo import get_collection
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Choose Gemini model
model = "gemini-2.0-flash"

STYLE_PROMPTS = {
    "formal": "Summarize the article very professionally and formally, suitable for business executives. Do not add any disclaimers or additional information.",
    "funny": "Summarize the article humorously, using jokes, memes, or sarcastic tone. Do not add any disclaimers or additional information.",
    "short": "Summarize the article in just ONE short sentence, capturing the key point. Do not add any disclaimers or additional information."
}

async def summarize_in_style(article_id: str, style: str):
    articles_collection = await get_collection("articles")

    article = await articles_collection.find_one({"_id": ObjectId(article_id)})
    if not article:
        return {"error": "Article not found"}

    content = article.get("content", "")
    if not content:
        return {"error": "No content available"}

    style_instruction = STYLE_PROMPTS.get(style.lower())
    if not style_instruction:
        return {"error": "Invalid style. Choose: formal, funny, short"}

    system_prompt = f"""
You are a smart AI summarizer.

Here is an article:
\"{content}\"

Task:
{style_instruction}

Respond ONLY with the summary.
"""

    try:
        response = client.models.generate_content(contents=[system_prompt], model=model)
        return {"summary_in_style": response.text.strip()}
    except Exception as e:
        print(f"Error in custom summary: {e}")
        return {"error": "Failed to generate custom summary"}
