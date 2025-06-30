from transformers import pipeline

_summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def summarize_text(prompt: str, transcript: str) -> str:
    """
    Combine prompt with transcript and generate a summary.
    """
    full_prompt = f"{prompt.strip()}\n{transcript.strip()}"
    result = _summarizer(full_prompt, max_length=512, do_sample=False)
    return result[0].get('summary_text') or result[0].get('generated_text')
