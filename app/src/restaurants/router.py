import os
import tempfile
import requests
import pandas as pd
from fastapi import Depends
from fastapi import APIRouter
from fastapi import UploadFile
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from src.models.models import food
from src.models.models import restaurant
from src.models.models import food_allergens
from src.database import get_async_session
from src.restaurants.schemas import RestaurantCreate


URL = os.environ.get('URL')
API_KEY = os.environ.get('API_KEY')

target_languages = ["CS", "EN", "DE", "ES", "FR", "UK"]


router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"]
)


def translate_to_json(text, to_list):
    output = {}
    for lang in target_languages:
        response = requests.post(URL, data={
        "auth_key": API_KEY,
        "text": text,
        "target_lang": lang
        })
        if to_list:
            output[lang] = [item.strip() for item in response.json()["translations"][0]["text"].split(",")]
        else:
            output[lang] = response.json()["translations"][0]["text"]
    return output


def convert_size(quantity, unit):
    conversion_factors = {
        'g': {
            'system': 'metric',            
            'conversion_factor': 0.035274,
            'converted_unit': 'oz'
        },
        'oz': {
            'system': 'imperial',              
            'conversion_factor': 28.3495,
            'converted_unit': 'g'
        },
        'lb': {
            'system': 'imperial',             
            'conversion_factor': 0.453592,
            'converted_unit': 'kg'          
        },
        'kg': {
            'system': 'metric',             
            'conversion_factor': 2.20462,
            'converted_unit': 'lb'              
        },
        'ml': {
            'system': 'metric',            
            'conversion_factor': 0.0338,
            'converted_unit': 'fl oz'
        },
        'l': {
            'system': 'metric',              
            'conversion_factor': 2.11338,
            'converted_unit': 'pt'
        },
        'fl oz': {
            'system': 'imperial',             
            'conversion_factor': 29.5735,
            'converted_unit': 'ml'          
        },
        'pt': {
            'system': 'imperial',             
            'conversion_factor': 0.473176,
            'converted_unit': 'l'              
        }
    }
    try:
        conversion = {conversion_factors[unit]["system"]: f"{round(quantity, 2)} {unit}", 
                  conversion_factors[conversion_factors[unit]["converted_unit"]]["system"]:
                      f"{round(quantity*conversion_factors[unit]['conversion_factor'], 2)} {conversion_factors[unit]['converted_unit']}"}
        
        return conversion
    
    except TypeError:
            print("Zadané číslo v neplatném formátu.")
            
    except KeyError:
            print("Nepodporovaná jednotka.")


@router.post("/")
async def add_restaurant(new_restaurant: RestaurantCreate, 
                         session: AsyncSession = Depends(get_async_session)
):
    # Inserting data into the restaurant table
    stmt = insert(restaurant).values(**new_restaurant.dict())
    await session.execute(stmt)
    await session.commit()

    return {"status": "success"}


@router.post("/menu")
async def add_menu(email: str, 
                   menu_file: UploadFile,
                   session: AsyncSession = Depends(get_async_session)):
    
    # Get restaurant id
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
            'size': convert_size(row.size, row.unit),
            'price': row.price,
            'currency': row.currency,
            'is_active': True,
            'restaurant_id': restaurant_id
        }
        
        query = select(food).where(
        food.c.food_name == data["food_name"],
        food.c.ingredients == data["ingredients"],
        food.c.diet_restriction == data["diet_restriction"],
        food.c.restaurant_id == restaurant_id)
        result = await session.execute(query)
        
        fetch_id = result.fetchone()
        if fetch_id:
            food_id = fetch_id[0]
            query = update(food).where(food.c.food_id == food_id).values(**data)
            await session.execute(query)

            query = delete(food_allergens).where(food_allergens.c.food_id == food_id)
            await session.execute(query)

            for allergen in row.allergens.split(','):
                if allergen.strip():
                    ins = insert(food_allergens).values([{'food_id': food_id, 'allergen_id': allergen.strip()}])
                    await session.execute(ins)

        else:
            ins = insert(food).values(**data).returning(food.c.food_id) 
            result = await session.execute(ins) 
            inserted_food_id = result.fetchone()[0] 
            print(f"Inserted row with food_id: {inserted_food_id}")
            
            for allergen in row.allergens.split(','):
                if allergen.strip():
                    ins = insert(food_allergens).values([{'food_id': inserted_food_id, 'allergen_id': allergen.strip()}])
                    await session.execute(ins)
        
    await session.commit()
    return {"status": "success"}


@router.get('/menu') 
async def get_menu(email: str, 
                   session: AsyncSession = Depends(get_async_session)
):
    """
    Maybe to remove this endpoint at all?
    And make the menu output only for clients...
    """
    query = select(restaurant.c.restaurant_id).where(restaurant.c.email == email)
    restaurant_id = await session.execute(query)
    
    query = select(food.c.food_name).where(food.c.restaurant_id == restaurant_id.fetchone()[0])
    result = await session.execute(query)
    
    return result.fetchone()[0]
    
