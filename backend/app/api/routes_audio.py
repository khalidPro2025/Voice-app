from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query, BackgroundTasks
from app.services.storage_s3 import upload_bytes, generate_presigned_url, list_objects, get_client
from app.core.config import settings
from uuid import uuid4
from pathlib import Path
import os
from app.db import AsyncSessionLocal
from app.models import Audio
from sqlalchemy import insert, select
from app.services.transcription import transcribe_and_update
import botocore

router = APIRouter()

# Helper: DB session provider for endpoints if needed
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/upload-audio-s3")
async def upload_audio_s3(background_tasks: BackgroundTasks, file: UploadFile = File(...), user: str | None = None, db = Depends(get_db)):
    ext = Path(file.filename).suffix or ".webm"
    # store uploaded bytes in temp file
    tmp_in = f"/tmp/{uuid4().hex}{ext}"
    content = await file.read()
    with open(tmp_in, "wb") as f:
        f.write(content)

    # try converting to opus/ogg using ffmpeg to have WhatsApp-like voice
    tmp_out = f"/tmp/{uuid4().hex}.ogg"
    final_path = tmp_in
    final_mime = file.content_type or "audio/webm"
    try:
        # convert with ffmpeg (best-effort)
        import subprocess
        subprocess.run([
            "ffmpeg", "-i", tmp_in,
            "-c:a", "libopus", "-b:a", "32k", "-vbr", "on",
            "-application", "voip",
            tmp_out, "-y"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(tmp_out, "rb") as f:
            data = f.read()
        final_path = tmp_out
        final_mime = "audio/ogg"
    except Exception:
        # fallback to uploaded bytes
        data = content

    # upload to S3/MinIO
    key = f"audios/{uuid4().hex}{Path(final_path).suffix}"
    try:
        upload_bytes(settings.AWS_BUCKET_NAME, key, data, content_type=final_mime)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

    # record metadata in DB
    size = os.path.getsize(final_path) if os.path.exists(final_path) else len(data)
    async with AsyncSessionLocal() as session:
        stmt = insert(Audio).values(
            key=key,
            filename=file.filename,
            content_type=final_mime,
            size=size,
            user=user
        ).returning(Audio.id)
        res = await session.execute(stmt)
        await session.commit()

    # schedule transcription in background (non-blocking)
    background_tasks.add_task(transcribe_and_update, key)

    # cleanup temp files
    try:
        if os.path.exists(tmp_in): os.remove(tmp_in)
        if os.path.exists(tmp_out): os.remove(tmp_out)
    except Exception:
        pass

    return {"status": "ok", "key": key}

@router.get("/audio/{key:path}")
def get_audio(key: str):
    s3 = get_client()
    try:
        obj = s3.get_object(Bucket=settings.AWS_BUCKET_NAME, Key=key)
    except botocore.exceptions.ClientError:
        raise HTTPException(status_code=404, detail="Audio not found")
    return StreamingResponse(
        obj["Body"],
        media_type=obj.get("ContentType", "application/octet-stream")
    )

from fastapi.responses import StreamingResponse

@router.get("/audio-url/{key:path}")
def get_presigned_url(key: str):
    url = generate_presigned_url(key)
    return {"url": url}

@router.get("/audios")
async def list_audios(limit: int = Query(50, ge=1, le=200), offset: int = 0):
    # read from DB
    async with AsyncSessionLocal() as session:
        q = select(Audio).limit(limit).offset(offset)
        res = await session.execute(q)
        audios = res.scalars().all()
        result = []
        for a in audios:
            result.append({
                "id": a.id,
                "key": a.key,
                "filename": a.filename,
                "content_type": a.content_type,
                "size": a.size,
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "user": a.user,
                "transcript": a.transcript
            })
    return result
