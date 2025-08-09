import asyncio
import json
import httpx

# Sample 7-day journal dummy data
sample_journal_entries = [
    {
        "title": "Starting Fresh",
        "content": "Today I decided to make some major changes in my life. I've been feeling stuck in my routine and need something new. Applied for a few new jobs and started planning a trip I've been putting off for months.",
        "emotions": [
            {"emotion": "excitement", "confidence": 0.78},
            {"emotion": "nervousness", "confidence": 0.65},
            {"emotion": "optimism", "confidence": 0.82}
        ],
        "created_at": "2024-01-15T08:30:00Z"
    },
    {
        "title": "Interview Prep Stress",
        "content": "Got a call back for an interview tomorrow! I'm excited but also terrified. Spent the whole day researching the company and practicing answers. I really want this opportunity but I'm worried I'll mess it up.",
        "emotions": [
            {"emotion": "nervousness", "confidence": 0.89},
            {"emotion": "excitement", "confidence": 0.76},
            {"emotion": "fear", "confidence": 0.68}
        ],
        "created_at": "2024-01-16T19:45:00Z"
    },
    {
        "title": "Nailed It!",
        "content": "The interview went amazing! I felt confident and the conversation flowed naturally. They seemed really impressed with my experience and we had great chemistry. Feeling so proud of myself for taking this leap.",
        "emotions": [
            {"emotion": "pride", "confidence": 0.92},
            {"emotion": "joy", "confidence": 0.85},
            {"emotion": "relief", "confidence": 0.79}
        ],
        "created_at": "2024-01-17T16:20:00Z"
    },
    {
        "title": "Waiting Game",
        "content": "It's been two days since the interview and I haven't heard back yet. My mind keeps going to worst-case scenarios. Maybe I didn't do as well as I thought? The uncertainty is killing me.",
        "emotions": [
            {"emotion": "nervousness", "confidence": 0.87},
            {"emotion": "disappointment", "confidence": 0.72},
            {"emotion": "confusion", "confidence": 0.64}
        ],
        "created_at": "2024-01-18T21:15:00Z"
    },
    {
        "title": "Life-Changing Call",
        "content": "THEY OFFERED ME THE JOB! I can't believe it's real. Better salary, better benefits, and work I'm actually passionate about. I said yes immediately. This feels like the beginning of a whole new chapter.",
        "emotions": [
            {"emotion": "joy", "confidence": 0.96},
            {"emotion": "excitement", "confidence": 0.94},
            {"emotion": "gratitude", "confidence": 0.88}
        ],
        "created_at": "2024-01-19T14:30:00Z"
    },
    {
        "title": "Reflection and Gratitude",
        "content": "Spent today calling family and friends to share the news. Everyone is so happy for me. Looking back at how scared I was just a week ago, I'm amazed at how much can change when you take a chance on yourself.",
        "emotions": [
            {"emotion": "gratitude", "confidence": 0.91},
            {"emotion": "love", "confidence": 0.83},
            {"emotion": "realization", "confidence": 0.77}
        ],
        "created_at": "2024-01-20T18:45:00Z"
    },
    {
        "title": "Ready for Adventure",
        "content": "Start the new job next Monday and booked that trip for next month! I feel like I'm finally living instead of just existing. This week taught me that fear is just excitement without breath. So grateful for this journey.",
        "emotions": [
            {"emotion": "excitement", "confidence": 0.93},
            {"emotion": "optimism", "confidence": 0.89},
            {"emotion": "gratitude", "confidence": 0.85}
        ],
        "created_at": "2024-01-21T20:00:00Z"
    }
]

async def test_routes():
    base_url = "http://localhost:8000"  # Adjust port if different
    
    async with httpx.AsyncClient() as client:
        print("Testing /emotions/ route:")
        print("=" * 50)
        
        # Test emotion route - corrected endpoint
        test_text = "I'm so excited about my new job but also nervous about the challenges ahead!"
        emotion_payload = {"text": test_text}
        
        try:
            response = await client.post(f"{base_url}/emotions/", json=emotion_payload)
            response.raise_for_status()
            emotions = response.json()
            print(f"Input: {test_text}")
            print(f"Emotions detected: {json.dumps(emotions, indent=2)}")
        except httpx.RequestError as e:
            print(f"Error calling emotion endpoint: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error {e.response.status_code}: {e.response.text}")
        
        print("\n" + "=" * 50)
        print("Testing /insights/quote route:")
        print("=" * 50)
        
        # Test quote route
        quote_payload = {"entries": sample_journal_entries}
        
        try:
            response = await client.post(f"{base_url}/insights/quote", json=quote_payload)
            response.raise_for_status()
            quote = response.json()
            print(f"Generated Quote: {json.dumps(quote, indent=2)}")
        except httpx.RequestError as e:
            print(f"Error calling quote endpoint: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error {e.response.status_code}: {e.response.text}")
        
        print("\n" + "=" * 50)
        print("Testing /insights/daily-summary route:")
        print("=" * 50)
        
        # Test daily summary route
        summary_payload = {"entries": sample_journal_entries}
        
        try:
            response = await client.post(f"{base_url}/insights/daily-summary", json=summary_payload)
            response.raise_for_status()
            summary = response.json()
            print(f"Generated Summary: {json.dumps(summary, indent=2)}")
        except httpx.RequestError as e:
            print(f"Error calling daily-summary endpoint: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error {e.response.status_code}: {e.response.text}")

if __name__ == "__main__":
    asyncio.run(test_routes())