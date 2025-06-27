from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_token_header

router = APIRouter(
    prefix="/emotions",
    tags=["emotions"],
    dependencies=[Depends(get_token_header)]
)

@router.get("/")
async def get_emotions():
    return "sadboy"