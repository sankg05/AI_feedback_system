import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash-lite"

def extract_json(text: str):
    """
    Extracts the first JSON object from a string.
    """
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in LLM response")

    json_str = text[start:end + 1]
    return json.loads(json_str)

def fallback_ai_output():
    return {
        "user_response": "Thank you for your feedback! Our team will review it shortly.",
        "summary": "User provided general feedback without structured details.",
        "recommended_actions": "Monitor feedback trends.",
        "status": "failed",
        "error": "LLM response not in JSON format"
    }

def process_review_with_gemini(rating: int, review_text: str):
    """
    Uses Gemini to generate:
    - User-facing response
    - Admin summary
    - Recommended actions
    """

    fallback_response = {
        "user_response": "Thank you for your feedback! Our team will review it shortly.",
        "summary": "No detailed feedback provided.",
        "recommended_actions": "Monitor feedback trends.",
        "status": "failed",
        "error": None
    }

    prompt = f"""
        You are an AI system embedded inside a production feedback platform.

        You MUST return a single valid JSON object.
        DO NOT include explanations, markdown, or extra text.
        DO NOT wrap the response in ``` or any formatting.
        ONLY return raw JSON.

        The JSON object MUST contain the following keys:

        1. "user_response":
        - A polite, empathetic, and professional message addressed directly to the user.
        - It should acknowledge their feedback and reflect the sentiment of the review.
        - Do NOT mention internal processes or analysis.
        - Tone should be friendly, reassuring, and concise.

        2. "summary":
        - A concise internal summary (1–2 sentences) of the user's feedback.
        - This summary is for administrators, not the user.
        - Capture key positives, negatives, or themes.

        3. "recommended_actions":
        - Clear, actionable internal recommendations for the business team.
        - Examples:
            - "Investigate reported service delays"
            - "Maintain current pricing strategy"
            - "Monitor recurring feedback about crowding"
        - Keep it brief and practical.

        IMPORTANT RULES:
        - If the review is empty, unclear, or extremely short, still return valid JSON.
        - In such cases, generate neutral but reasonable defaults.
        - Always return ALL three keys.

        User Review:
        \"\"\"{review_text}\"\"\"

        JSON RESPONSE:

        {{
        "user_response": "...",
        "summary": "...",
        "recommended_actions": "..."
        }}
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=300
            )
        )
        
        try:
            raw_text = response.text.strip()
            parsed = extract_json(raw_text)

            return {
                "user_response": parsed["user_response"],
                "summary": parsed["summary"],
                "recommended_actions": parsed["recommended_actions"],
                "status": "processed",
                "error": None
            }

        except Exception as e:
            fallback = fallback_ai_output()
            fallback["error"] = str(e)
            return fallback

    except Exception as e:
        fallback_response["error"] = str(e)
        return fallback_response
