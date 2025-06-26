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

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f"""
Analyze the following journal entry and identify the **single most predominant emotion** from the provided GoEmotions list. Choose only one emotion.

GoEmotions List: {', '.join(go_emotions_list)}

Journal Entry: \"{journal_entry_text}\"

Return the output strictly in the following JSON format with the confidence score as a number with 3 decimal places:
{{
"emotion": "<identified_emotion>",
"confidence": <confidence_score_as_decimal_with_3_places>
}}

Example of proper formatting:
{{
"emotion": "disappointment",
"confidence": 0.875
}}
"""
)

try:
    # Parse the response text as JSON
    emotion_output = json.loads(response.text)
    
    # Format the output to ensure confidence has 3 decimal places
    formatted_output = {
        "emotion": emotion_output["emotion"],
        "confidence": round(float(emotion_output["confidence"]), 3)
    }
    
    # Print the formatted JSON output
    print(json.dumps(formatted_output, indent=2))
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    print(f"Raw model response: {response.text}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    print(f"Raw model response: {response.text}")