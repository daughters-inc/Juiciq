from fastapi import FastAPI, HTTPException
from src.scrapenews import ScrapeNews, CategoryDoesNotExist
from redis import Redis
import json

app = FastAPI()
redis = Redis(host='redis', port=6379)


@app.get("/")
async def root():
    return {"message": "Welcome to Juiciq!"}


@app.get("/news/{category}")
async def analyze(category: str) -> dict:
    try:
        if redis.get(category):
            news = json.loads(redis.get(category).decode)
        else:
            news = ScrapeNews(category).scrape()
    except CategoryDoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"result": news}
