import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Upgraded Model Slugs
MODEL_NAME = "google/gemini-2.5-flash-lite"

# Directory configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Create directories if they do not exist
for directory in [ASSETS_DIR, UPLOADS_DIR, REPORTS_DIR, DATA_DIR]:
    os.makedirs(directory, exist_ok=True)
