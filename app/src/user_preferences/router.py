from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.models import user_preferences
from src.user_preferences.schemas import PreferenceCreate

router = APIRouter(
    prefix="/preferences",
    tags=["Preferences"]
)


@router.post("/")
async def add_user_preferences(new_user_preferences: PreferenceCreate,                               
                               session: AsyncSession = Depends(get_async_session)):
    # if id already exist
    stmt = insert(user_preferences).values(**new_user_preferences.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/")
async def get_user_preferences(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(user_preferences).where(user_preferences.c.user_id == user_id)
    result = await session.execute(query)
    preferences = []
    for row in result.all():
        preference = {
            "user_id": row[0],
            "preferred_ingredients": row[1],
            "allergens": row[2]
        }
        preferences.append(preference)
    return preferences

