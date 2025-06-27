from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..gemini import getEmotion

class EmotionRequest(BaseModel):
    text: str

router = APIRouter(
    prefix="/emotions",
    tags=["emotions"],
)

@router.post("/")
async def get_emotions(request: EmotionRequest):
    emotion_result = await getEmotion(request.text)
    return emotion_result