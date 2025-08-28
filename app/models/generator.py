import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.core.constants import MODEL_ID
from app.core.config import HUGGINGFACE_HUB_TOKEN  # ← import token here

_tokenizer = None
_model = None

def get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID,
            token=HUGGINGFACE_HUB_TOKEN  # ← pass token
        )
    return _tokenizer

def get_model():
    global _model
    if _model is None:
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            token=HUGGINGFACE_HUB_TOKEN  # ← pass token
        )
        if not torch.cuda.is_available():
            _model = _model.to("cpu")
    return _model
