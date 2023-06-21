from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.models import user_preferences
from src.user_preferences.schemas import PreferenceCreate
from check_flag import set_completion_flag


router = APIRouter(
    prefix="/preferences",
    tags=["Preferences"]
)

# ingredients_list = []

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
    
    set_completion_flag()
    return {"status": "success"}


@router.post("/check")
async def check_user_preferences(user_id: int,
                               session: AsyncSession = Depends(get_async_session)
):
    """
    Checking the completion of the questionnaire.
    Args:
        user_id (int)
    Returns:
        status: success
    """
    stmt = select(user_preferences.c.user_id).where(
        user_preferences.c.user_id == user_id)
    result = await session.execute(stmt)
    user_id = result.scalar_one_or_none()

    if user_id:
        return True
    else:
        return False
    