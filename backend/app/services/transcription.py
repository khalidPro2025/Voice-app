import os
import shutil
import whisper
from app.services.storage_s3 import get_client
from app.core.config import settings
from app.db import AsyncSessionLocal
from app.models import Audio
import asyncio

# Load the model once on import (heavy)
# Consider using a smaller model like 'tiny' or 'base' if limited resources
try:
    model = whisper.load_model("base")
except Exception as e:
    model = None
    # If model can't be loaded, transcription will be skipped

def download_from_s3_to(path: str, key: str):
    s3 = get_client()
    with open(path, "wb") as f:
        s3.download_fileobj(settings.AWS_BUCKET_NAME, key, f)

def transcribe_sync(local_path: str) -> str:
    if model is None:
        return ""
    result = model.transcribe(local_path)
    return result.get("text", "")

async def transcribe_and_update(key: str):
    """
    Download object from S3, transcribe it (whisper), and update DB (audio.transcript).
    This runs in background; uses its own DB session.
    """
    tmp_dir = "/tmp/voice_processing"
    os.makedirs(tmp_dir, exist_ok=True)
    local_path = os.path.join(tmp_dir, os.path.basename(key))

    # download
    try:
        download_from_s3_to(local_path, key)
    except Exception as e:
        # cannot download -> exit
        return

    # run transcription (blocking) in thread to avoid blocking event loop
    loop = asyncio.get_event_loop()
    text = await loop.run_in_executor(None, transcribe_sync, local_path)

    # update DB
    async with AsyncSessionLocal() as session:
        # find audio by key
        res = await session.execute(
            __import__("sqlalchemy").select(Audio).where(Audio.key == key)
        )
        audio = res.scalars().first()
        if audio:
            audio.transcript = text
            session.add(audio)
            await session.commit()

    # cleanup
    try:
        os.remove(local_path)
        # optional: remove tmp_dir if empty
        if not os.listdir(tmp_dir):
            shutil.rmtree(tmp_dir)
    except Exception:
        pass
