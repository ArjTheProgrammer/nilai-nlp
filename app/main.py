from fastapi import Depends, FastAPI

from .routers import emotions, insights

app = FastAPI()

app.include_router(emotions.router)
app.include_router(insights.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}