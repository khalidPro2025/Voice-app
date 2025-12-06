import asyncio
from app.core.config import settings
from app.db import engine
from app.models import Base as ModelsBase
from app.services.storage_s3 import get_client
import botocore

def ensure_bucket():
    s3 = get_client()
    try:
        # list to check exist
        s3.head_bucket(Bucket=settings.AWS_BUCKET_NAME)
        print("Bucket exists:", settings.AWS_BUCKET_NAME)
    except botocore.exceptions.ClientError:
        # create bucket
        print("Creating bucket:", settings.AWS_BUCKET_NAME)
        s3.create_bucket(Bucket=settings.AWS_BUCKET_NAME)
        print("Bucket created")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(ModelsBase.metadata.create_all)
        print("DB tables ensured")

def main():
    # ensure bucket first (MinIO might be still spinning up but usually accessible via docker-compose depends_on)
    try:
        ensure_bucket()
    except Exception as e:
        print("Warning: cannot ensure bucket yet (it may not be ready). You can create it manually. Error:", e)

    # create DB tables
    try:
        asyncio.run(create_tables())
    except Exception as e:
        print("Error creating DB tables:", e)

if __name__ == "__main__":
    main()
