def format_prompt_for_claude(prompt: str, transcript: str, user_type: str, note_type: str) -> str:
    return (
        f"{prompt.strip()}\n"
        f"This session was conducted by a {user_type}, and the note type is '{note_type}'.\n"
        f"Below is the original transcript. Format this into a well-structured, readable summary:\n"
        f"Transcript:\n{transcript.strip()}"
    )
