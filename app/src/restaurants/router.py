import json
import tempfile
from fastapi import APIRouter, Depends, UploadFile
import requests
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert 


import pandas as pd

from src.database import get_async_session
from src.models.models import restaurant, food, food_allergens
from src.restaurants.schemas import RestaurantCreate


url = "https://api-free.deepl.com/v2/translate"
api_key = "63ba9046-f75c-649e-9113-db66591d0bfd:fx"

target_languages = ["CS", "EN", "DE", "ES", "FR", "UK"]

router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"]
)

def translate_to_json(text, to_list):
    output = {}
    for lang in target_languages:
        response = requests.post(url, data={
        "auth_key": api_key,
        "text": text,
        "target_lang": lang
        })
        if to_list:
            output[lang] = [item.strip() for item in response.json()["translations"][0]["text"].split(",")]
        else:
            output[lang] = response.json()["translations"][0]["text"]
    return json.dumps(output, ensure_ascii=False)


@router.post("/")
async def add_restaurant(new_restaurant: RestaurantCreate, 
                                  session: AsyncSession = Depends(get_async_session)):
    
    # Inserting data into the restaurant table
    stmt = insert(restaurant).values(**new_restaurant.dict())
    await session.execute(stmt)
    
    await session.commit()
    return {"status": "success"}



@router.post("/menu")
async def add_menu(email: str, 
                   menu_file: UploadFile,
                   session: AsyncSession = Depends(get_async_session)):
    
    query = select(restaurant.c.restaurant_id).where(restaurant.c.email == email)
    restaurant_id = await session.execute(query)
    restaurant_id = restaurant_id.fetchone()[0]
    
    
    # Create a temporary file and write into it the contents of the downloaded file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        menu_file.file.seek(0)
        tmp.write(menu_file.file.read())
        tmp.close()
        # Reading an Excel file with pandas
        df = pd.read_excel(tmp.name)
        df = df.fillna('')
        
    # Update previous food to non active
    upd = update(food).where(food.c.restaurant_id == restaurant_id).values(is_active=False)
    await session.execute(upd)

    for row in df.itertuples(index=False):

        data = {
            'food_name': translate_to_json(row.food_name, to_list=False),
            'category_name': translate_to_json(row.category_name, to_list=False),
            'dish_picture_url': row.dish_picture_url,
            'ingredients': translate_to_json(row.ingredients, to_list=True),
            'diet_restriction': translate_to_json(row.diet_restriction, to_list=True),
            'nutritional_values': row.nutritional_values,
            'size': row.size,
            'unit': row.unit,
            'price': row.price,
            'currency': row.currency,
            'is_active': True,
            'restaurant_id': restaurant_id
        }
        
        ins = insert(food).values(**data).returning(food.c.food_id) 
        result = await session.execute(ins) 
        inserted_food_id = result.fetchone()[0] 
        print(f"Inserted row with food_id: {inserted_food_id}")
        
        # ins = insert(food).values(**data).on_conflict_do_update(
        #     index_elements=['food_name', 'restaurant_id'],set_={'is_active': True}).returning(food.c.food_id)
        # result = await session.execute(ins)
        # inserted_food_id = result.fetchone()[0]
        # print(f"Inserted row with food_id: {inserted_food_id}")
        
        
        for allergen in row.allergens.split(','):
            if allergen.strip():
                ins = insert(food_allergens).values([{'food_id': inserted_food_id, 'allergen_id': allergen.strip()}])
                await session.execute(ins)
        

    await session.commit()
    return {"status": "success"}


@router.get('/menu')
async def get_menu(email: str, session: AsyncSession = Depends(get_async_session)):
    # get restaurant id
    query = select(restaurant.c.restaurant_id).where(restaurant.c.email == email)
    restaurant_id = await session.execute(query)
    
    query = select(food.c.food_name).where(food.c.restaurant_id == restaurant_id.fetchone()[0])
    result = await session.execute(query)
    print(result.fetchone())
    
    return result.fetchone()[0]

    
