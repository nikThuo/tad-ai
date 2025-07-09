import os
from openai import OpenAI
from dotenv import load_dotenv
from app.services.openai_formatter import format_prompt_for_openai

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def summarize_text(prompt: str, transcript: str, user_type: str, note_type: str) -> str:
    full_prompt = format_prompt_for_openai(prompt, transcript, user_type, note_type)

    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0.5,
        max_tokens=800,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes therapy session transcripts into well-structured notes."},
            {"role": "user", "content": full_prompt}
        ]
    )

    return response.choices[0].message.content.strip()
