import pandas as pd
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from sqlalchemy import select, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.models import food, user_preferences, user_history, food_allergens, restaurant


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)

templates = Jinja2Templates(directory="templates")

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

@router.get('/{restaurant_id}', response_class=HTMLResponse)
async def display_menu( 
       restaurant_id: int,
       request: Request,
       session: AsyncSession = Depends(get_async_session)):
    
    ordered_food_ids = [55, 50, 9]
    user_id = 2
    language = "EN"

    stmt = select(restaurant.c.name).where(restaurant.c.restaurant_id == restaurant_id)
    result = await session.execute(stmt)
    restaurant_name = result.fetchone()[0]

    stmt = select(user_preferences).where(user_preferences.c.user_id == user_id)
    result = await session.execute(stmt)
    user_prefers = result.fetchall()[0]

    stmt = select(food, food_allergens).select_from(food.join(food_allergens, food.c.food_id == food_allergens.c.food_id)).where(food.c.food_id.in_(ordered_food_ids))
    menu = await session.execute(stmt)
    menu_items = menu.fetchall()

    transformed_data = []

    for menu_item in menu_items:
        food_name = menu_item.food_name
        allergen_id = menu_item.allergen_id
        
        for item in transformed_data:
            if item['food_name'] == food_name:
                item['allergen_ids'].append(allergen_id)
                break
        else:
            transformed_data.append({'food_id': menu_item.food_id, 'food_name': food_name, 'allergen_ids': [allergen_id], 'category_name': menu_item.category_name, 'ingredients': menu_item.ingredients,
                                     'diet_restriction': menu_item.diet_restriction, 'nutritional_values': menu_item.nutritional_values, 'size': menu_item.size,
                                     'price': menu_item.price, 'currency': menu_item.currency})
    
    return templates.TemplateResponse("menu.html", {"request": request, "restaurant_id": restaurant_id, "menu_items": transformed_data, 
                                                    "language": language, "metric_system": user_prefers.metric_system,
                                                    "diet_restriction": user_prefers.diet_restriction, "allergens": user_prefers.allergens,
                                                    "restaurant_name": restaurant_name, "user_id": user_id})

class Rating(BaseModel):
    rating: str
    userId: int
    foodId: int

@router.post('/{restaurant_id}', response_class=HTMLResponse)
async def rate_food(request: Request, rating: Rating, session: AsyncSession = Depends(get_async_session)):
    if rating.rating == "neutral":
        stmt = delete(user_history).where((user_history.c.id_user == rating.userId) &(user_history.c.id_food == rating.foodId))
        
    else:
        stmt = select(user_history).where(user_history.c.id_user == rating.userId, user_history.c.id_food == rating.foodId)
        result = await session.execute(stmt)
        existing = result.fetchone()

        if existing is None:
            stmt = user_history.insert().values(id_user=rating.userId, id_food=rating.foodId, rating=rating.rating)
            print("vložen")
        
        else:
            stmt = user_history.update().where(user_history.c.id_user == rating.userId, user_history.c.id_food == rating.foodId).values(rating=rating.rating)
            print("updatovan")
    
    await session.execute(stmt)
    await session.commit()
    print(rating)
    return templates.TemplateResponse("menu.html", {"request": request})
