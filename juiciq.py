from fastapi import FastAPI
from src.scrapenews import ScrapeNews
from redis import Redis
import json

app = FastAPI()
redis = Redis(host='redis', port=6379)


@app.get("/")
async def root():
    return {"message": "Welcome to Juiciq!"}


@app.get("/news/{category}")
async def analyze(category: str) -> dict:
    if redis.get(category):
        news = redis.get(category)
        news = json.loads(news.decode())
    else:
        news = ScrapeNews(category).scrape()
    return {"result": news}
