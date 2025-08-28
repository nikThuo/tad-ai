from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes_transcribe import router as transcribe_router
from app.api.v1.routes_expand import router as expand_router
from app.api.v1.finetuning import router as finetuned_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe_router, prefix="/v1", tags=["Transcription"])
app.include_router(expand_router, prefix="/v1", tags=["Expand"])
app.include_router(finetuned_router, prefix="/v1", tags=["Finetuned"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
