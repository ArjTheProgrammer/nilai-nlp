from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

class EmotionRequest(BaseModel):
    text: str

router = APIRouter(
    prefix="/emotions",
    tags=["emotions"],
)

@router.post("/")
async def get_emotions(request: EmotionRequest):
    emotion_result = f"emotion mo ay tungkol sa : {request.text} ay: sadboy"
    return emotion_result