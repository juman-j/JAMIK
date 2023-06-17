import json
import pandas as pd
from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from src.models.models import food
from src.models.models import user_preferences
from src.models.models import user_history
from src.menu.schemas import AddRating


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


async def get_menu_df(restaurant_id, session):
    """
    Returns the dataset with the actual meals at a certain restaurant

    Args:
        restaurant_id (int)
        session (AsyncSession)

    Returns:
        menu_df: Pandas dataframe
    """
    stmt = select(food).where(food.c.restaurant_id == restaurant_id,
                              food.c.is_active == True)
    menu = await session.execute(stmt)
    munu = menu.fetchall()
    menu_list = []

    for row in munu:
        one_meal = []
        for column in row:
            if type(column) != dict:
                one_meal.append(column)
            else:
                one_meal.append(column.get('EN'))
        menu_list.append(one_meal)
    
    menu_df = pd.DataFrame(data=menu_list, columns=food.columns)
    
    return menu_df


async def get_ingredients(user_id, session):
    """
    Returns the list of ingredients that the user selected in the questionnaire

    Args:
        user_id (int)
        session (AsyncSession)

    Returns:
        list_ingredients: list
    """
    stmt = select(user_preferences.c.preferred_ingredients).where(user_preferences.c.user_id == user_id)
    list_ingredients = await session.execute(stmt)
    list_ingredients = list_ingredients.fetchall()[0][0]

    return list_ingredients


async def get_history(user_id, session):
    """
    Returns the id of dishes that were rated by a certain user

    Args:
        user_id (int)
        session (AsyncSession)

    Returns:
        history: list
    """
    try:
        stmt = select(user_history.c.id_food).where(user_history.c.id_user == user_id,
                                                    user_history.c.rating == 1)
        history = await session.execute(stmt)
        history = [food_id[0] for food_id in history.fetchall()]
    except AttributeError:
        print("User hasn't rated any dishes yet")
    return history


def ml(menu_df, list_ingredients, history):
    dummy = [11, 2]
    return dummy


async def get_sorted_menu(sorted_list, session):
    """
    Returns the sorted menu in a list format with dictionaries with individual dishes 

    Args:
        sorted_list (list): The list of food_id that we got as a result of machine learning sorting
        session (AsyncSession)

    Returns:
        sorted_menu: list of dictionaries
    """
    keys = select(food)
    keys = await session.execute(keys)
    keys = keys.keys()._keys
    
    sorted_menu = []
    for row in sorted_list:
        row = select(food).where(food.c.food_id == row)
        row = await session.execute(row)
        
        row = dict(zip(keys, list(row.fetchone())))
        sorted_menu.append(row)
    
    return sorted_menu


@router.get('/{restaurant_id}')
async def get_menu(user_id: int, 
       restaurant_id: int,
       session: AsyncSession = Depends(get_async_session)
):
    # Prepare input for machine learning
    menu_df = await get_menu_df(restaurant_id, session)
    list_ingredients = await get_ingredients(user_id, session)
    history = await get_history(user_id, session)

    # ML
    sorted_list = ml(menu_df, list_ingredients, history)
    # Final result
    sorted_menu = await get_sorted_menu(sorted_list, session)

    return sorted_menu


@router.post("/user_history")
async def add_rating(new_rating: AddRating,
                     session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(user_history).values(**new_rating.dict())
    await session.execute(stmt)
    await session.commit()

    return {"status": "success"}

