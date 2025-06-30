def transcribe_audio(model, audio_path: str) -> str:
    """
    Transcribes the given audio file using either OpenAI or Faster-Whisper.

    Args:
        model: Whisper model instance.
        audio_path (str): Path to the .wav audio file.

    Returns:
        str: Transcribed text.
    """
    result = model.transcribe(audio_path)

    # OpenAI Whisper returns a dict
    if isinstance(result, dict) and "text" in result:
        return result["text"]

    # Faster-Whisper returns a tuple (segments, info)
    elif isinstance(result, tuple):
        segments, _ = result
        return " ".join([segment.text for segment in segments])

    raise ValueError("Unexpected transcription result format.")
