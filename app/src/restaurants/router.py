import tempfile
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

import pandas as pd

from src.database import get_async_session
from src.models.models import restaurant, menu
from src.restaurants.schemas import RestaurantCreate


router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"]
)


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
    
    # Создаем временный файл и записываем в него содержимое загруженного файла
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        menu_file.file.seek(0)
        tmp.write(menu_file.file.read())
        tmp.close()
        # Reading an Excel file with pandas
        df = pd.read_excel(tmp.name)
    
    # convert to json
    menu_json = df.to_json(orient="records")
    
    query = select(restaurant.c.id).where(restaurant.c.email == email)
    restaurant_id = await session.execute(query)
    # Inserting data into the menu table
    stmt2 = insert(menu).values(restaurant_id = restaurant_id.fetchone()[0], 
                                menu = menu_json)
    
    await session.execute(stmt2)
    await session.commit()
    return {"status": "success"}
    

