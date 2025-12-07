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

class Settings(BaseSettings):
    DATABASE_URL: str
    MQTT_BROKER: str
    MQTT_PORT: int
    AWS_ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_BUCKET_NAME: str

    PREALERT_THRESHOLD: float = 10
    ALERT_THRESHOLD: float = 30
    CRITICAL_THRESHOLD: float = 60

settings = Settings()
