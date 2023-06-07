from fastapi import APIRouter, Depends
# from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
# from src.models.models import restaurant, menu
# from src.menu.schemas import 


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


@router.get("/")
async def get_menu(session: AsyncSession = Depends(get_async_session)):
    pass

