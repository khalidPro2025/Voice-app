import json
import asyncio
from asyncio_mqtt import Client
from ..core.config import settings
from ..db import SessionLocal
from ..models import Inondation
from sqlalchemy import insert
from app.services.alert_service import check_and_alert

TOPIC = "cleansen/inondation/#"

async def mqtt_worker():
    async with Client(settings.MQTT_BROKER, settings.MQTT_PORT) as client:
        await client.subscribe(TOPIC)

        async with client.unfiltered_messages() as messages:
            async for msg in messages:
                payload = json.loads(msg.payload.decode())

                async with SessionLocal() as db:
                    stmt = insert(Inondation).values(
                        device_id=payload["device_id"],
                        zone=payload["zone"],
                        niveau_mm=payload["niveau_mm"],
                        status="ok",
                        raw=payload
                    )
                    await db.execute(stmt)
                    await db.commit()
check_and_alert(device_id, zone, niveau)
