from fastapi import APIRouter, HTTPException
from app.schemas.requests import ExpandIn, ExpandOut, TokenUsage
from app.services.text_expander import generate_expansion
from app.core.constants import MODEL_ID

router = APIRouter()

@router.post("/finetuned_summarize", response_model=ExpandOut)
def expand_endpoint(payload: ExpandIn):
    pass

@router.post("/finetuned_expand", response_model=ExpandOut)
def expand_endpoint(payload: ExpandIn):
    pass
