from apscheduler.schedulers.background import BackgroundScheduler
from app.services.fetch_news import fetch_and_store_news
import asyncio

scheduler = BackgroundScheduler()

def start_news_scheduler():
    """
    Start the scheduler to fetch news daily.
    """
    # Schedule fetch_and_store_news to run every day at 00:00 UTC
    scheduler.add_job(fetch_news_task, 'cron', hour=0, minute=0)
    scheduler.start()

def fetch_news_task():
    """
    Wrapper for async fetch_and_store_news inside a blocking scheduler.
    """
    asyncio.run(fetch_and_store_news(category="technology", country="us"))
