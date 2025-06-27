import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

journal_entry_text = "I am happy that everyone in okay today!"

# The full list of GoEmotions categories
go_emotions_list = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring",
    "confusion", "curiosity", "desire", "disappointment", "disapproval",
    "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
    "joy", "love", "nervousness", "optimism", "pride", "realization",
    "relief", "remorse", "sadness", "surprise", "neutral"
]

async def getEmotion(journal_entry):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""
    Analyze the following journal entry and identify up to 5 emotions from the provided GoEmotions list. Rank them by confidence score in descending order.

    GoEmotions List: {', '.join(go_emotions_list)}

    Journal Entry: {journal_entry}

    Return the output strictly in the following JSON format with confidence scores as numbers with 2 decimal places:
    {{
      "emotions": [
        {{ "emotion_name": "<emotion1>", "confidence": <confidence_score> }},
        {{ "emotion_name": "<emotion2>", "confidence": <confidence_score> }},
        {{ "emotion_name": "<emotion3>", "confidence": <confidence_score> }}
      ]
    }}

    Rules:
    - Include 1-5 emotions maximum
    - Order by confidence score (highest first)
    - Confidence scores should be between 0.00 and 1.00
    - Use exactly 2 decimal places for confidence scores

    Example of proper formatting:
    {{
      "emotions": [
        {{ "emotion_name": "joy", "confidence": 0.98 }},
        {{ "emotion_name": "sadness", "confidence": 0.75 }},
        {{ "emotion_name": "annoyance", "confidence": 0.60 }}
      ]
    }}
    """
    )

    try:
        response_text = response.text.strip()
        
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise ValueError("No JSON found in response")
        
        json_text = response_text[start_idx:end_idx]
        
        emotion_output = json.loads(json_text)

        # Validate and format the emotions array
        formatted_emotions = []
        for emotion_data in emotion_output.get("emotions", [])[:5]:  # Limit to 5 emotions
            formatted_emotion = {
                "emotion_name": emotion_data["emotion_name"],
                "confidence": round(float(emotion_data["confidence"]), 2)
            }
            formatted_emotions.append(formatted_emotion)

        formatted_output = {
            "emotions": formatted_emotions
        }

        print(json.dumps(formatted_output, indent=2))
        
        return formatted_output
    except json.JSONDecodeError as e:
        return {"error": f"failed to parse JSON: {response.text}"}
    except Exception as e:
        return {"error": f"failed to get emotion: {e}"}