from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Text, Float, JSON, TIMESTAMP
from sqlalchemy.sql import func
from app.db import Base
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Audio(Base):
    __tablename__ = "audios"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)   # s3 key
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    size = Column(BigInteger, nullable=True)
    duration = Column(Integer, nullable=True)  # duration in seconds (optional)
    user = Column(String, nullable=True)
    transcript = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Inondation(Base):
    __tablename__ = "inondations"

    id = Column(Integer, primary_key=True)
    device_id = Column(String)
    zone = Column(String)
    niveau_mm = Column(Float)
    status = Column(String)
    raw = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=text("now()"))
