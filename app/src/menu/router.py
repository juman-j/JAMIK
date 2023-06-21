import numpy as np
import pandas as pd

from fastapi import Depends
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import update
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer

from src.models.models import food
from src.models.models import allergen
from src.models.models import user_history
from src.models.models import food_allergens
from src.models.models import user_preferences
from src.menu.schemas import AddRating
from src.database import get_async_session
from check_flag import check_completion_flag, set_completion_flag_false
import asyncio


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
    
    columns = ['food_id', 
               'food_name', 
               'category_name', 
               'dish_picture_url', 
               'ingredients', 
               'diet_restriction', 
               'nutritional_values', 
               'size', 
               'price', 
               'currency', 
               'is_active', 
               'restaurant_id']
    
    menu_df = pd.DataFrame(data=menu_list, columns=columns)

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
    try:        
        stmt = select(user_preferences.c.preferred_ingredients).where(user_preferences.c.user_id == user_id)
        ingredients_list = await session.execute(stmt)
        ingredients_list = ingredients_list.fetchall()[0][0]

    except IndexError:
        error_message = 'The user did not complete the questionnaire. More specifically: the field with the ingredients.'
        return JSONResponse(status_code=400, content={"detail": error_message})

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
    df['ingredients_str'] = df['ingredients'].apply(lambda x: str(x))
    df['ingredients_str'] = df['ingredients_str'].str.strip("[]").str.replace("'", "")
    df = df[["food_id", "food_name", "ingredients_str", "category_name"]]

    # Get a new unique ID for each new row
    if type(list_ingredients) == list and len(list_ingredients) != 0:
      new_rows = pd.DataFrame(columns=df.columns)
      new_ids = []
      # Iterate over the new ingredients and create a new row for each
      for count, ingredient in enumerate(list_ingredients, 1):
          new_row = df.iloc[0].copy()  # Copy the first row to get the structure
          new_row['food_id'] = df['food_id'].max() + count
          new_row['ingredients_str'] = str(ingredient)
          new_row['food_name'] = ""
          new_row['category_name'] = ""
          new_rows.loc[len(new_rows)] = new_row
          # new_rows = new_rows.append(new_row, ignore_index=False)
          new_ids.append(new_row['food_id'])

      # Concatenate the original DataFrame and the new rows DataFrame
      df = pd.concat([df, new_rows], ignore_index=False)
      df = df.set_index('food_id')
      history_list = history_list + new_ids

    name_vectorizer = TfidfVectorizer(max_features=1000)
    name_vectors = name_vectorizer.fit_transform(df['food_name'] + " " + df['category_name'] + " " + df['ingredients_str'])

    # Create a preprocessed dataframe with the dense matrix
    df_final = pd.DataFrame(name_vectors.toarray())
    df_final.index = df.index

    def recommend_meals(menu_list, history_list, df_final):
      past_features = df_final.loc[history_list]
      new_features = df_final.loc[menu_list]
      # vytvori se podprostor vzdalenosti se starymi jidly
      nn = NearestNeighbors()
      nn.fit(past_features)

      # najit vzdalenost k nejblizsich sousedu pro nova jidla
      k = len(history_list) # jako k sousedu = vsechna stara jidla
      distances, indices = nn.kneighbors(new_features, n_neighbors=k)
      avg_distances = distances.mean(axis=1)

      menu_list = np.array(menu_list)
      sorted_ids = menu_list[avg_distances.argsort()]
      return sorted_ids.tolist()

    sorted_list = recommend_meals(menu_list, history_list, df_final)

    return sorted_list


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
    while True:
        flag_value = check_completion_flag()
        if flag_value == True:
            set_completion_flag_false()
            break
        await asyncio.sleep(0.5)

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
    try:
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
    
    except IntegrityError:
        error_message = 'Please try other parameters'
        return JSONResponse(status_code=400, content={"detail": error_message})


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

