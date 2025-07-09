from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.core.constants import NOTE_TYPE_MAP
from app.models.whisper import get_whisper_model
from app.models.summarizer import summarize_text
from app.models.summarizer_claude import summarize_text as summarize_claude
from app.models.summarizer_openai import summarize_text as summarize_openai
from app.utils.audio import convert_to_wav, get_file_hash, cleanup_files
from app.services.transcriber import transcribe_audio
import tempfile, shutil, os
import re


router = APIRouter()

transcript_cache = {}

@router.post("/transcribe-live")
async def transcribe_live(
    user_type: str = Form(...),
    note_type: str = Form(...),
    prompt: str = Form(...),
    audio_file: UploadFile = File(...)
):
    return await _transcribe(user_type, note_type, prompt, audio_file, model_size="base")


@router.post("/transcribe-recorded")
async def transcribe_recorded(
    user_type: str = Form(...),
    note_type: str = Form(...),
    prompt: str = Form(...),
    audio_file: UploadFile = File(...)
):
    return await _transcribe(user_type, note_type, prompt, audio_file, model_size="large-v3")


async def _transcribe(user_type, note_type, prompt, audio_file, model_size):
    if user_type not in NOTE_TYPE_MAP:
        raise HTTPException(status_code=400, detail="Invalid user_type")
    if note_type not in NOTE_TYPE_MAP[user_type]:
        raise HTTPException(status_code=400, detail="Invalid note_type for given user_type")

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[-1]) as tmp_orig:
        temp_orig_path = tmp_orig.name
        shutil.copyfileobj(audio_file.file, tmp_orig)

    temp_wav_path = temp_orig_path + ".wav"

    try:
        convert_to_wav(temp_orig_path, temp_wav_path)
        audio_hash = get_file_hash(temp_wav_path)

        if audio_hash in transcript_cache:
            raw_transcript = transcript_cache[audio_hash]
        else:
            model = get_whisper_model(model_size)
            raw_transcript = transcribe_audio(model, temp_wav_path)
            transcript_cache[audio_hash] = raw_transcript

        summary = summarize_text(prompt, raw_transcript)

        return {
            "original_transcript": raw_transcript,
            "formatted_text": summary,
            "prompt_used": prompt,
            "metadata": {
                "user_type": user_type,
                "note_type": note_type
            }
        }

    finally:
        cleanup_files([temp_orig_path, temp_wav_path])

# @router.post("/summarize-text-claude")
# async def summarize_text_claude(
#     user_type: str = Form(...),
#     note_type: str = Form(...),
#     prompt: str = Form(...),
#     long_text: str = Form(...)
# ):
#     if user_type not in NOTE_TYPE_MAP:
#         raise HTTPException(status_code=400, detail="Invalid user_type")
#     if note_type not in NOTE_TYPE_MAP[user_type]:
#         raise HTTPException(status_code=400, detail="Invalid note_type for given user_type")
#
#     formatted_text = await summarize_claude(prompt, long_text, user_type, note_type)
#     return {
#         "original_transcript": long_text,
#         "formatted_text": formatted_text,
#         "prompt_used": prompt,
#         "metadata": {
#             "user_type": user_type,
#             "note_type": note_type
#         }
#     }

@router.post("/summarize-text")
async def summarize_text_openai(
    user_type: str = Form(...),
    note_type: str = Form(...),
    prompt: str = Form(...),
    long_text: str = Form(...)
):
    if user_type not in NOTE_TYPE_MAP:
        raise HTTPException(status_code=400, detail="Invalid user_type")
    if note_type not in NOTE_TYPE_MAP[user_type]:
        raise HTTPException(status_code=400, detail="Invalid note_type for given user_type")

    summary = await summarize_openai(prompt, long_text, user_type, note_type)

    cleaned_text = re.sub(r"\s+", " ", summary.replace("\n", " ")).strip()

    return {
        "original_transcript": long_text,
        "formatted_text": cleaned_text,
        "prompt_used": prompt,
        "metadata": {
            "user_type": user_type,
            "note_type": note_type
        }
    }