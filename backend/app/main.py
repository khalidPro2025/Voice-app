from fastapi import FastAPI
from app.api import routes_audio
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title="Voice Upload API")

# very permissive CORS for dev; tighten in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_audio.router, prefix="/api")

