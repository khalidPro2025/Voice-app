import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
from typing import Optional

def get_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.AWS_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",
    )

def upload_bytes(bucket: str, key: str, data: bytes, content_type: str):
    s3 = get_client()
    s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
    return True

def generate_presigned_url(key: str, expires_in: int = None) -> str:
    s3 = get_client()
    expires = expires_in or settings.PRESIGNED_EXPIRES_IN
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": key},
        ExpiresIn=expires,
    )

def list_objects(prefix: Optional[str] = ""):
    s3 = get_client()
    resp = s3.list_objects_v2(Bucket=settings.AWS_BUCKET_NAME, Prefix=prefix)
    return resp.get("Contents", [])
