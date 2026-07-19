import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY is missing")

client = genai.Client(api_key=api_key.strip())

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Reply only with: API key works",
)

print(response.text)