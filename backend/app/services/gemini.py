import re
import json
from flask import jsonify
from app.config import Config

class GeminiAPIError(Exception):
    pass

def handle_gemini_error(e):
    return jsonify({"status": "error", "message": str(e)}), 400

client = None
if Config.GEMINI_API_KEY:
    from google import genai
    client = genai.Client(api_key=Config.GEMINI_API_KEY)

def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    if not client:
        raise GeminiAPIError("Please add your Gemini API key to the .env file and restart the server.")
    try:
        resp = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return resp.text
    except Exception as e:
        raise GeminiAPIError(f"Gemini API Error: {e}")

def ask_gemini_json(prompt: str):
    """Send a prompt expecting JSON back. Returns parsed dict/list."""
    raw = ask_gemini(prompt)
    # Strip markdown code fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    cleaned = re.sub(r"```\s*$", "", cleaned.strip())
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise GeminiAPIError(f"Failed to parse AI response as JSON: {e}. Raw response: {raw}")
