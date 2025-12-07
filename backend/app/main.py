import asyncio
from .api.routes_inondation import router
from .services.mqtt_listener import mqtt_worker
from fastapi import FastAPI
from app.api import routes_audio
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title="Voice Upload API")

app = FastAPI(title="CleanSen360 Flood Detection")

app.include_router(router)

# very permissive CORS for dev; tighten in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_audio.router, prefix="/api")

@app.on_event("startup")
async def startup():
    asyncio.create_task(mqtt_worker())
