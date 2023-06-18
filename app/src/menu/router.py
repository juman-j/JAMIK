import pandas as pd
from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from src.models.models import food
from src.models.models import user_preferences
from src.models.models import user_history
from src.models.models import food_allergens
from src.models.models import allergen
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


@router.get("/{restaurant_id}")
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
    """
    One user can only rate one dish once, 
    but if he decides to change the rating, 
    this data will be updated in the user_history table.

    Args:
        new_rating (AddRating): schema
        session (AsyncSession)

    Returns:
        status: success
    """
    stmt = select(user_history.c.rating).where(user_history.c.id_food == new_rating.id_food,
                                              user_history.c.id_user == new_rating.id_user)
    result = await session.execute(stmt)
    rating = result.scalar_one_or_none()
    
    if rating == None:
        stmt = insert(user_history).values(**new_rating.dict())
        await session.execute(stmt)
        await session.commit()
    elif rating != new_rating.rating:
        stmt = update(user_history).where(
            user_history.c.id_food == new_rating.id_food, 
            user_history.c.id_user == new_rating.id_user).values(
                rating = new_rating.rating)
        await session.execute(stmt)
        await session.commit()
    else:
        pass


    return {"status": "success"}


@router.get("/{food_id}/allergens")
async def get_allergen(food_id: int, 
                       session: AsyncSession = Depends(get_async_session)
):
    """
    Returns the list of allergens for a specific dish 

    Args:
        food_id (int)
        session (AsyncSession)

    Returns:
        allergen_list: list of dictionaries
    """
    stmt = select(food_allergens.c.allergen_id).where(food_allergens.c.food_id == food_id)
    result = await session.execute(stmt)
    allergen_id_list = [row[0] for row in result.fetchall()]

    keys = select(allergen)
    keys = await session.execute(keys)
    keys = keys.keys()._keys

    allergen_list = []
    for row in allergen_id_list:
        row = select(allergen).where(allergen.c.allergen_id == row)
        row = await session.execute(row)

        row = dict(zip(keys, list(row.fetchone())))
        allergen_list.append(row)

    return allergen_list