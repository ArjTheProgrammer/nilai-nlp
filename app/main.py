from fastapi import Depends, FastAPI
from .gemini import getDailyQuote
from .routers import emotions, insights

app = FastAPI()

app.include_router(emotions.router)
app.include_router(insights.router)


@app.get("/")
async def root():
    return {"message": "Hello! Welcome to Nilai's AI part. Hacker ka ba bakit ka nandito? 😑"}