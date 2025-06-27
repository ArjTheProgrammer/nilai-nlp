from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/emotions",
    tags=["emotions"],
)

@router.get("/")
async def get_emotions():
    return "sadboy"