"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

# Load environment variables from services/.env
load_dotenv('.env')
load_dotenv('services/.env')

# PolzaAI API key
POLZAAI_API_KEY = os.getenv("POLZAAI_API_KEY")

# Council members - list of PolzaAI model identifiers
COUNCIL_MODELS = [
    "google/gemini-3-flash-preview",
    "anthropic/claude-3.5-haiku",
    "openai/gpt-4o-mini",
    "x-ai/grok-4-fast"
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "google/gemini-3-flash-preview"

# PolzaAI API endpoint
POLZAAI_API_URL = "https://api.polza.ai/api/v1/chat/completions"

