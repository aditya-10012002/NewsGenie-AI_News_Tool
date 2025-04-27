import os
from google import genai
from app.db.mongo import get_collection
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Choose Gemini model
model = "gemini-2.0-flash"

async def fetch_all_summaries():
    articles_collection = await get_collection("articles")
    cursor = articles_collection.find({"summary": {"$ne": None}})
    
    summaries = []
    async for article in cursor:
        summaries.append(f"- {article['title']}: {article['summary']}")
    
    return "\n".join(summaries)

async def answer_query(user_query: str):
    all_summaries = await fetch_all_summaries()

    system_prompt = f"""
You are a helpful AI assistant. 
Here is the latest news summarized:
{all_summaries}

Do not include any disclaimers or additional information.
Based only on this information, answer the following user query accurately:
\"{user_query}\"
"""

    try:
        response = client.models.generate_content(contents=[system_prompt], model=model)
        return {"answer": response.text.strip()}
    except Exception as e:
        print(f"Error in chatbot response: {e}")
        return {"error": "Failed to generate answer"}
