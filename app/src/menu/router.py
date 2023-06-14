from fastapi import APIRouter, Depends

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.models import food, user_preferences
# from src.menu.schemas import 


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


# @router.get("/")
# async def get_menu(user_id: int, 
#                    session: AsyncSession = Depends(get_async_session)):
#     pass


@router.get('/')
async def ml(user_id: int, 
       restaurant_id: int,
       session: AsyncSession = Depends(get_async_session)):
    stmt = select(food).where(food.c.restaurant_id == restaurant_id)
    full_menu = await session.execute(stmt)
    print(full_menu.all())
    
    stmt = select(user_preferences.c.preferred_ingredients).where(user_preferences.c.id == user_id)
    user_ingr = await session.execute(stmt)
    print(user_ingr.all())
    
    return None
    
    