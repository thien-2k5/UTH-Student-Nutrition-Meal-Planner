import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "uth_student_nutrition_secret_key_12345")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", 
        f"sqlite:///{DB_DIR / 'food.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Optional Gemini AI API Config
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    # Fallback/alternative OpenAI API Config
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
