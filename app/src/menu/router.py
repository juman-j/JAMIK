import pandas as pd
from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy import delete, select
from sqlalchemy import update
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from src.models.models import food
from src.models.models import allergen
from src.models.models import user_history
from src.models.models import food_allergens
from src.models.models import user_preferences
from src.menu.schemas import AddRating


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)

async def get_menu_list(restaurant_id, session):
    """
    Get a list of food_id for a specific restaurant.

    Args:
        restaurant_id (int)
        session (AsyncSession)

    Returns:
        menu_list: list of food_id
    """
    stmt = select(food.c.food_id).where(food.c.restaurant_id == restaurant_id, 
                                        food.c.is_active == True)
    menu_list = await session.execute(stmt)
    menu_list = [food_id[0] for food_id in menu_list.fetchall()]

    return menu_list


async def get_df(menu_list, history_list, session):
    """
    Returns the dataset with the actual meals at a certain restaurant

    Args:
        restaurant_id (int)
        session (AsyncSession)

    Returns:
        menu_df: Pandas dataframe
    """
    stmt = select(food).where(food.c.food_id.in_(menu_list + history_list))
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
    menu_df.to_csv('vstupni_df_pro_ml.csv')
    print('done')
    
    return menu_df


async def get_ingredients_list(user_id, session):
    """
    Returns the list of ingredients that the user selected in the questionnaire

    Args:
        user_id (int)
        session (AsyncSession)

    Returns:
        list_ingredients: list
    """
    stmt = select(user_preferences.c.preferred_ingredients).where(user_preferences.c.user_id == user_id)
    ingredients_list = await session.execute(stmt)
    ingredients_list = ingredients_list.fetchall()[0][0]

    return ingredients_list


async def get_history_list(user_id, session):
    """
    Returns the id of dishes that were rated by a certain user

    Args:
        user_id (int)
        session (AsyncSession)

    Returns:
        history_list: list
    """
    try:
        stmt = select(user_history.c.id_food).where(user_history.c.id_user == user_id,
                                                    user_history.c.rating == 1)
        history_list = await session.execute(stmt)
        history_list = [food_id[0] for food_id in history_list.fetchall()]
    except AttributeError:
        print("User hasn't rated any dishes yet")
    return history_list


def ml(df, list_ingredients, history_list, menu_list):
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
    """
    Several functions are called to prepare the data for 
    feeding it into the machine learning part.
    Next, the ml function is invoked, 
    which takes the results of the preparatory functions as input and
    returns the sorted food_id list.
    The final function collects the menu from the food_id list and 
    outputs a list of dishes in dictionary format, 
    where each dish is defined in 5 languages.

    Args:
        user_id (int)
        restaurant_id (int)
        session (AsyncSession)

    Returns:
        sorted_menu: list of dictionaries
    """
    # Prepare input for machine learning
    ingredients_list = await get_ingredients_list(user_id, session)
    menu_list = await get_menu_list(restaurant_id, session)
    history_list = await get_history_list(user_id, session)
    df = await get_df(menu_list, history_list, session)

    # ML
    sorted_list = ml(df, ingredients_list, history_list, menu_list)

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
    If the user sets the same rating again, 
    the previous action will be cancelled.

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
    elif rating == new_rating.rating:
            stmt = delete(user_history).where(user_history.c.id_food == new_rating.id_food,
                                              user_history.c.id_user == new_rating.id_user)
            await session.execute(stmt)
            await session.commit()


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