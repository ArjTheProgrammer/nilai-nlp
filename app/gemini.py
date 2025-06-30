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

    Return the output strictly in the following JSON format with confidence scores as numbers with 5 decimal places:
    {{
      "emotions": [
        {{ "emotion": "<emotion1>", "confidence": <confidence_score> }},
        {{ "emotion": "<emotion2>", "confidence": <confidence_score> }},
        {{ "emotion": "<emotion3>", "confidence": <confidence_score> }}
      ]
    }}

    Rules:
    - if the LLM identified more than 1 emotion, 5 emotions is maximum and the confidence of the emotions should be minimum 0.80
    - Order by confidence score (highest first)
    - Confidence scores should be between 0.00 and 1.00
    - Use exactly 2 decimal places for confidence scores

    Example of proper formatting:
    {{
      "emotions": [
        {{ "emotion": "joy", "confidence": 0.98 }},
        {{ "emotion": "sadness", "confidence": 0.75 }},
        {{ "emotion": "annoyance", "confidence": 0.60 }}
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
                "emotion": emotion_data["emotion"],
                "confidence": round(float(emotion_data["confidence"]), 2)
            }
            formatted_emotions.append(formatted_emotion)

        print(json.dumps(formatted_emotions, indent=2))
        
        return formatted_emotions
    except json.JSONDecodeError as e:
        return {"error": f"failed to parse JSON: {response.text}"}
    except Exception as e:
        return {"error": f"failed to get emotion: {e}"}