from faster_whisper import WhisperModel

_model_cache = {}

def get_whisper_model(size: str = "large-v3") -> WhisperModel:
    """
    Load and cache Whisper model by size.
    """
    if size not in _model_cache:
        _model_cache[size] = WhisperModel(size, compute_type="int8", device="cpu")
    return _model_cache[size]
