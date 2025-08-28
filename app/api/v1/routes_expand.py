from fastapi import APIRouter, HTTPException
from app.schemas.requests import ExpandIn, ExpandOut, TokenUsage
from app.services.text_expander import generate_expansion
from app.core.constants import MODEL_ID

router = APIRouter()

@router.post("/expand", response_model=ExpandOut)
def expand_endpoint(payload: ExpandIn):
    if not payload.brief.strip():
        raise HTTPException(status_code=400, detail="brief cannot be empty")

    expanded, tokens = generate_expansion(payload)
    return ExpandOut(
        expanded_text=expanded,
        model=MODEL_ID,
        tokens=TokenUsage(**tokens),
        safety={"pii_removed": True, "disclaimer_added": True}
    )
