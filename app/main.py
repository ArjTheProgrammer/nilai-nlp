from fastapi import Depends, FastAPI

from .routers import emotions

app = FastAPI()


app.include_router(emotions.router)



@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}