from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.models import user_preferences
from user_preferences.schemas import PreferenceCreate

router = APIRouter(
    prefix="/preferences",
    tags=["Preferences"]
)


@router.get("/")
async def get_user_preferences(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(user_preferences).where(user_preferences.c.user_id == user_id)
    result = await session.execute(query)
    preferences = []
    for row in result.all():
        preference = {
            "user_id": row[0],
            "preferred_cuisine": row[1],
            "preferred_ingredients": row[2],
            "disliked_ingredients": row[3],
            "allergens": row[4],
            "nutritional_preferences": row[5],
        }
        preferences.append(preference)
    return preferences


@router.post("/")
async def add_user_preferences(new_user_preferences: PreferenceCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(user_preferences).values(**new_user_preferences.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}