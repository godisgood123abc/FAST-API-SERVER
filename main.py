from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
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

    # 🛠️ DEBUG: show full Groq response
    try:
        json_response = response.json()
    except Exception as e:
        return {"error": "Invalid JSON response", "raw": response.text}

    if response.status_code != 200:
        return {"error": json_response}

    # 🧠 Check where message is
    try:
        return {"response": json_response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {
            "error": "Could not extract message",
            "full_response": json_response
        }
