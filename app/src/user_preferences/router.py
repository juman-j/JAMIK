from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
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
                               session: AsyncSession = Depends(get_async_session)
):
    """
    This endpoint writes the user's preferences to the database. 
    If this user has already entered his preferences, the preferences will be updated.

    Args:
        new_user_preferences (PreferenceCreate): 
                                                user_id: int
                                                preferred_ingredients: list
                                                diet_restriction: list = None
                                                metric_system: str
                                                allergens: list = None
        session (AsyncSession)

    Returns:
        status: success
    """
    stmt = select(user_preferences.c.user_id).where(
        user_preferences.c.user_id == new_user_preferences.user_id)
    result = await session.execute(stmt)
    user_id = result.scalar_one_or_none()
    
    if user_id == None:
        stmt = insert(user_preferences).values(**new_user_preferences.dict())
        await session.execute(stmt)
        await session.commit()
    else:
        stmt = update(user_preferences).where(
            user_preferences.c.user_id == new_user_preferences.user_id).values(
                **new_user_preferences.dict())
        await session.execute(stmt)
        await session.commit()
    
    return {"status": "success"}

