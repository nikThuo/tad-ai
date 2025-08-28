from pydantic import BaseModel, Field
from typing import Optional
from app.core.constants import Audience, Tone

class ExpandIn(BaseModel):
    brief: str = Field(..., min_length=3, description="Short note to expand.")
    audience: Audience
    tone: Tone
    # The following three arrive in payload but are IGNORED / not parsed:
    target_words: Optional[int] = None
    reading_level: Optional[str] = None
    include_california_context: Optional[bool] = None

class TokenUsage(BaseModel):
    prompt: int
    completion: int

class ExpandOut(BaseModel):
    expanded_text: str
    model: str
    tokens: TokenUsage
    safety: dict
