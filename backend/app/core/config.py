from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_ENDPOINT_URL: str = "http://minio:9000"
    AWS_ACCESS_KEY_ID: str = "minioadmin"
    AWS_SECRET_ACCESS_KEY: str = "minioadmin"
    AWS_BUCKET_NAME: str = "voice-uploads"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/voice_db"

    # Presigned URL expiry (seconds)
    PRESIGNED_EXPIRES_IN: int = 3600

    class Config:
        env_file = ".env"

settings = Settings()
