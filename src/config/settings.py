import os
from dotenv import load_dotenv


def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()


def get_llm_config():
    """Get LLM configuration from environment variables"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in .env file")
    
    return {
        "config_list": [{
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "api_key": api_key,
            "base_url": "https://api.groq.com/openai/v1",
        }],
        "temperature": 0.4
    }