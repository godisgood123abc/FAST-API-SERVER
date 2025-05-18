from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Define request schema
class ChatRequest(BaseModel):
    prompt: str

# Define the /chat POST endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"error": "API key missing in .env"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": request.prompt}]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    try:
        json_response = response.json()
    except Exception:
        return {"error": "Invalid JSON response", "raw": response.text}

    if response.status_code != 200:
        return {"error": json_response}

    try:
        return {"response": json_response["choices"][0]["message"]["content"]}
    except Exception:
        return {
            "error": "Could not extract message",
            "full_response": json_response
        }
