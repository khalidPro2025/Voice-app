from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import get_db
from ..models import Inondation

router = APIRouter(prefix="/api")

@router.get("/inondations")
async def get_inondations(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Inondation))
    return res.scalars().all()
