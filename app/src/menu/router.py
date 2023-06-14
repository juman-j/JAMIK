import pandas as pd
from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.models import food, user_preferences, user_history


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


@router.get('/')
async def ml(user_id: int, 
       restaurant_id: int,
       session: AsyncSession = Depends(get_async_session)):
    # menu restaurace
    stmt = select(food).where(food.c.restaurant_id == restaurant_id,
                              food.c.is_active == True)
    menu = await session.execute(stmt)
    menu_items = menu.fetchall()
    menu_list = []

    for row in menu_items:
        one_meal = []
        for i in row:
            if type(i) != dict:
                one_meal.append(i)
            else:
                one_meal.append(i.get('EN'))
        menu_list.append(one_meal)
    
    menu_df = pd.DataFrame(data = menu_list, columns=food.columns)
    
    # seznam ingredienci z dotazniku
    stmt = select(user_preferences.c.preferred_ingredients).where(user_preferences.c.user_id == user_id)
    user_ingr = await session.execute(stmt)
    list_ingredients = user_ingr.fetchall()[0]    

    # seznam food_id z historie uzivatele
    try:
        stmt = select(user_history.c.id_food).where(user_history.c.user_id == user_id,
                                                    user_history.c.rating == 1)
        history = await session.execute(stmt)
        food_id_list = history.all()
        
    except AttributeError:
        print("tabulka user_history je prazdna")

    return None

    