from fastapi import FastAPI
from app.api import news, summarize, recommend, chatbot, trending, custom_summary, favorites, auth
from app.scheduler.news_scheduler import start_news_scheduler
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="News Aggregator and Summarizer",
    description="Personalized news feed with summarization and recommendations",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start News Scheduler
start_news_scheduler()

# Include API routers
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(summarize.router, prefix="/summarize", tags=["Summarization"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(trending.router, prefix="/trending", tags=["Trending"])
app.include_router(custom_summary.router, prefix="/custom-summary", tags=["Custom Summary"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Welcome to the Personalized News Aggregator API!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
