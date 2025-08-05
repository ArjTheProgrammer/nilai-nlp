import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# The full list of GoEmotions categories
GO_EMOTIONS_LIST = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring",
    "confusion", "curiosity", "desire", "disappointment", "disapproval",
    "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
    "joy", "love", "nervousness", "optimism", "pride", "realization",
    "relief", "remorse", "sadness", "surprise", "neutral"
]


async def getEmotion(journal_entry):
    """Analyze journal entry and identify emotions using GoEmotions taxonomy."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(f"""
        Analyze the following journal entry and identify at least 1 and up to 5 emotions from the provided GoEmotions list. 
        Rank them by confidence score in descending order.

        GoEmotions List: {', '.join(GO_EMOTIONS_LIST)}

        Journal Entry: {journal_entry}

        Return the output strictly in the following JSON format:
        {{
          "emotions": [
            {{ "emotion": "<emotion1>", "confidence": <confidence_score> }},
            {{ "emotion": "<emotion2>", "confidence": <confidence_score> }}
          ]
        }}

        Rules:
        - ALWAYS identify at least 1 emotion from the GoEmotions list (use "neutral" if no clear emotion is present)
        - If multiple emotions are identified, maximum 5 emotions with confidence minimum 0.60
        - If only one emotion is identified, confidence can be as low as 0.50
        - Order by confidence score (highest first)
        - Confidence scores should be between 0.00 and 1.00
        - Use exactly 2 decimal places for confidence scores
        """)

        response_text = response.text.strip()
        
        # Extract JSON from response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise ValueError("No JSON found in response")
        
        json_text = response_text[start_idx:end_idx]
        emotion_output = json.loads(json_text)

        # Validate and format emotions
        formatted_emotions = []
        for emotion_data in emotion_output.get("emotions", [])[:5]:
            formatted_emotion = {
                "emotion": emotion_data["emotion"],
                "confidence": round(float(emotion_data["confidence"]), 2)
            }
            formatted_emotions.append(formatted_emotion)

        if not formatted_emotions:
            formatted_emotions = [{"emotion": "neutral", "confidence": 0.50}]

        return formatted_emotions

    except (json.JSONDecodeError, Exception) as e:
        print(f"Error analyzing emotions: {e}")
        return [{"emotion": "neutral", "confidence": 0.50}]


async def getDailyQuote(journal_entries):
    """Generate an inspiring quote based on recent journal entries."""
    if not journal_entries:
        raise ValueError("No journal entries provided")
    
    entries_text = "\n\n".join([
        f"Title: {entry['title']}\nContent: {entry['content']}\nEmotions: {entry.get('emotions', [])}\nDate: {entry['created_at']}"
        for entry in journal_entries
    ])
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(f"""
        Based on the following journal entries from the past 7 days, provide an inspiring and relevant quote with explanation.
        
        Journal Entries:
        {entries_text}
        
        Analyze the emotional patterns, themes, and experiences. Then provide a quote that:
        1. Relates to their current emotional state or journey
        2. Offers encouragement, wisdom, or perspective
        3. Helps them reflect on their experiences
        4. Only use quotes from stoic philosophers

        Rules:
        1. The format is heavily inspired from The Daily Stoic by Ryan Holiday
        2. Make the title creative and meaningful
        3. The explanation should focus on the timeless wisdom of the quote itself, not explicitly connecting it to the journal entries
        4. Write the explanation in Ryan Holiday's style - accessible, practical, and relatable to modern life
        5. Use contemporary examples and scenarios that make ancient wisdom relevant today
        6. Write with clarity and conviction, as Holiday does in The Daily Stoic

        Return strictly in JSON format:
        {{
          "title": "Creative title for the reflection",
          "quote": "The actual quote text",
          "author": "Author name",
          "citation": "Source or book if applicable",
          "explanation": "Write in Ryan Holiday's distinctive style from The Daily Stoic - make ancient wisdom accessible and practical for modern readers. Use contemporary examples, clear language, and focus on actionable insights. Length can vary naturally based on the depth of the wisdom being shared."
        }}
        """)
        
        response_text = response.text.strip()
        
        # Extract JSON from response (same logic as getEmotion)
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise ValueError("No JSON found in response")
        
        json_text = response_text[start_idx:end_idx]
        quote_output = json.loads(json_text)
        
        return quote_output
        
    except Exception as e:
        print(f"Error generating quote: {e}")
        return {
            "title": "Daily Reflection",
            "quote": "The journey of self-discovery begins with honest reflection.",
            "author": "Anonymous",
            "citation": "",
            "explanation": "Continue your journaling practice - insights come with consistency and self-awareness."
        }


async def getDailySummary(journal_entries):
    """Generate a thoughtful summary of the past week's journal entries."""
    if not journal_entries:
        raise ValueError("No journal entries provided")
    
    entries_text = "\n\n".join([
        f"Date: {entry['created_at'][:10]}\nTitle: {entry['title']}\nContent: {entry['content']}\nEmotions: {entry.get('emotions', [])}"
        for entry in journal_entries
    ])
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(f"""
        Analyze the following journal entries from the past 7 days and create a thoughtful weekly summary:
        
        Journal Entries (Past 7 Days):
        {entries_text}
        
        Create a weekly reflection that:
        1. Identifies emotional patterns and trends over the week
        2. Highlights significant events, growth, or challenges
        3. Notes how the person's mindset has evolved
        4. Offers gentle insights and supportive observations
        5. Recognizes progress and areas for continued growth
        6. Connects themes across the different days
        
        Write in a warm, supportive tone as if you're a thoughtful observer who understands the journey of personal growth.
        Focus on the overall patterns and evolution rather than day-by-day details.
        Be encouraging while remaining authentic and grounded.
        
        Return strictly in JSON format:
        {{
          "summary": "A 3-4 paragraph reflection on their past 7 days, focusing on patterns, growth, and insights written in a supportive yet insightful tone",
          "key_themes": ["theme1", "theme2", "theme3"],
          "emotional_trends": {{
            "dominant_emotions": ["emotion1", "emotion2"], 
            "emotional_arc": "Brief description of how emotions evolved over the week",
            "notable_shifts": "Any significant emotional changes or breakthroughs observed"
          }}
        }}
        """)
        
        response_text = response.text.strip()
        
        # Extract JSON from response (same logic as getEmotion)
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise ValueError("No JSON found in response")
        
        json_text = response_text[start_idx:end_idx]
        summary_output = json.loads(json_text)
        
        return summary_output
        
    except Exception as e:
        print(f"Error generating summary: {e}")
        return {
            "summary": "Your journaling journey continues to unfold with each entry, revealing patterns of growth and self-discovery. Each reflection adds another layer to your understanding of yourself and your experiences.",
            "key_themes": ["self-reflection", "personal growth", "mindful awareness"],
            "emotional_trends": {
                "dominant_emotions": ["contemplative", "introspective"],
                "emotional_arc": "Steady progress in self-awareness and emotional understanding",
                "notable_shifts": "Continued commitment to personal growth through reflective practice"
            }
        }