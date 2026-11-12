import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=api_key)

def generate_gtm_content(prompt: str) -> str:
    response = client.models.generate_content(
        model='gemini-1.5-pro',
        contents=prompt,
    )
    return response.text

if __name__ == "__main__":
    print("Gemini GTM Helper Initialized successfully.")
