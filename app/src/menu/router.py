from fastapi import APIRouter, Depends

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.models import food, user_preferences, user_history
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
    stmt = select(food).where(food.c.restaurant_id == restaurant_id,
                              food.c.is_active == True)
    menu = await session.execute(stmt)
    
    menu_items = menu.fetchall()
    
    for row in menu_items:
        for i in row:
            gg = []
            if type(i) == dict:
                print(i)
        
        
    print(f' только англ меню  {len(menu_items)}')
    
    
    
    
    
    
    
    
    
    stmt = select(user_preferences.c.preferred_ingredients).where(user_preferences.c.user_id == user_id)
    user_ingr = await session.execute(stmt)
    print(f'список ингредиентов пользователя: {user_ingr.one()}')

    try:
        stmt = select(user_history.c.id_food).where(user_history.c.user_id == user_id,
                                                    user_history.c.rating == 1)
        history = await session.execute(stmt)
        print(f'блюда, которые пользователь оценил: {history.all()}')
    except AttributeError:
        print("tabulka user_history je prazdna")
        

    return None
    
    