import tempfile
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

import pandas as pd

from database import get_async_session
from models.models import restaurant, menu
from restaurants.schemas import RestaurantCreate


router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"]
)


@router.post("/")
async def add_restaurant(new_restaurant: RestaurantCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(restaurant).values(**new_restaurant.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.post("/menu")
async def add_menu(restaurant_id: int, menu_file: UploadFile, session: AsyncSession = Depends(get_async_session)):
    # Создаем временный файл и записываем в него содержимое загруженного файла
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        menu_file.file.seek(0)
        tmp.write(menu_file.file.read())
        tmp.close()

        # Чтение Excel-файла с помощью pandas
        df = pd.read_excel(tmp.name)
    
    # Преобразование меню в формат JSON
    menu_json = df.to_json(orient="records")
    
    # Сохранение меню в базу данных
    stmt = insert(menu).values(menu_id=restaurant_id, menu=menu_json)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

