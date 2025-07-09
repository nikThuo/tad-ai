# app/models/summarizer_claude.py

import os
import httpx
from dotenv import load_dotenv
from app.services.claude_formatter import format_prompt_for_claude

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

if not ANTHROPIC_API_KEY:
    raise ValueError("Missing ANTHROPIC_API_KEY in your environment (.env) file.")

HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

async def summarize_text(prompt: str, transcript: str, user_type: str, note_type: str) -> str:
    """
    Send the formatted prompt to Claude and return a summarized, well-formatted text.
    """
    full_prompt = format_prompt_for_claude(prompt, transcript, user_type, note_type)

    payload = {
        "model": "claude-3-sonnet-20240229",  # Use 'claude-3-opus-20240229' if you have access
        "max_tokens": 800,
        "temperature": 0.5,
        "system": "You are a helpful assistant that formats therapy session transcripts into readable notes.",
        "messages": [
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(CLAUDE_API_URL, headers=HEADERS, json=payload)

        try:
            response.raise_for_status()
            json_response = response.json()
            return json_response["content"][0]["text"]
        except Exception as e:
            raise RuntimeError(f"Claude API failed: {e}\nDetails: {response.text}")
