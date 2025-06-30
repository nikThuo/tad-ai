import hashlib
import os
from pydub import AudioSegment

def convert_to_wav(input_path, output_path):
    """Convert any audio/video file to .wav format using pydub (FFmpeg)"""
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")

def get_file_hash(file_path):
    """Return SHA256 hash of the given file (used for caching)"""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def cleanup_files(paths):
    """Remove temporary files"""
    for path in paths:
        try:
            os.remove(path)
        except Exception:
            pass
