import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    if GEMINI_API_KEY == 'your_gemini_api_key_here':
        GEMINI_API_KEY = ''
    
    # Example MongoDB URI for future phase
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/genmotor')
