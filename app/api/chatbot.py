from fastapi import FastAPI, Request
import os
import httpx

app = FastAPI()

GROQ_API_URL = "https://api.groq.com/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/chat")
async def chat_with_bot(request: Request):
    body = await request.json()
    user_input = body.get("message")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "user", "content": user_input}]
            }
        )
    return res.json()
