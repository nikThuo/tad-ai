def format_prompt_for_openai(prompt: str, transcript: str, user_type: str, note_type: str) -> str:
    return (
        f"{prompt.strip()}\n"
        f"This session was conducted by a {user_type}, and the note type is '{note_type}'.\n"
        f"Below is the original transcript. Please summarize and format it for readability:\n"
        f"{transcript.strip()}"
    )
