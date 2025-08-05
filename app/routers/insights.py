from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..gemini import getDailyQuote, getDailySummary

class JournalEntry(BaseModel):
    title: str
    content: str
    emotions: Optional[List[dict]]
    created_at: str

class QuoteRequest(BaseModel):
    entries: List[JournalEntry]

class DailySummaryRequest(BaseModel):
    entries: List[JournalEntry]
    userId: str

router = APIRouter(
    prefix="/insights",
    tags=["insights"],
)

@router.post("/quote")
async def get_daily_quote(request: QuoteRequest):
    try:
        quote_result = await getDailyQuote(request.entries)
        return quote_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate daily quote: {str(e)}")

@router.post("/daily-summary")
async def get_daily_summary(request: DailySummaryRequest):
    try:
        summary_result = await getDailySummary(request.entries)
        return summary_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate daily summary: {str(e)}")