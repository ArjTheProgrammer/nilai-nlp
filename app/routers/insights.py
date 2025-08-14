from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
from ..gemini import getDailyQuote, getDailySummary, getEmotion

class JournalEntry(BaseModel):
    title: str
    content: str
    emotions: List[dict]
    created_at: str

class QuoteRequest(BaseModel):
    entries: List[JournalEntry]

class DailySummaryRequest(BaseModel):
    entries: List[JournalEntry]

class EmotionRequest(BaseModel):
    text: str

router = APIRouter(
    prefix="/insights",
    tags=["insights"],
)

@router.post("/quote")
async def get_daily_quote(request: QuoteRequest):
    try:
        # Convert Pydantic models to dictionaries
        entries_dict = [entry.model_dump() for entry in request.entries]
        quote_result = await getDailyQuote(entries_dict)
        return quote_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate daily quote: {str(e)}")

@router.get("/summary")
async def get_summary(entries: str):
    try:
        # Parse the entries from query parameter
        entries_list = json.loads(entries)
        summary_result = await getDailySummary(entries_list)
        
        # Ensure the response is valid JSON
        if isinstance(summary_result, str):
            try:
                # Try to parse as JSON to validate
                json.loads(summary_result)
                return {"summary": summary_result}
            except json.JSONDecodeError:
                # If it's not valid JSON, wrap it
                return {"summary": summary_result}
        
        return summary_result
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid entries format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")

@router.post("/daily-summary")
async def get_daily_summary(request: DailySummaryRequest):
    try:
        # Convert Pydantic models to dictionaries
        entries_dict = [entry.model_dump() for entry in request.entries]
        summary_result = await getDailySummary(entries_dict)
        
        # Ensure the response is valid JSON
        if isinstance(summary_result, str):
            try:
                # Try to parse as JSON to validate
                parsed = json.loads(summary_result)
                return parsed
            except json.JSONDecodeError:
                # If it's not valid JSON, wrap it
                return {"summary": summary_result}
        
        return summary_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate daily summary: {str(e)}")