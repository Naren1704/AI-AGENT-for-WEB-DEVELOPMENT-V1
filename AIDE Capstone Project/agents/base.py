from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from config.settings import GEMINI_MODEL, RETRY_CONFIG

def initialize_model():
    """Initialize the Gemini model"""
    model = Gemini(
        model=GEMINI_MODEL,
        retry_options=RETRY_CONFIG
    )
    print("✅ Environment setup complete.")
    return model