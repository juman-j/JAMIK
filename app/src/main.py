from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.models.models import User
from src.auth.base_config import auth_backend, fastapi_users, current_user
from src.auth.schemas import UserCreate, UserRead

from src.user_preferences.router import router as router_preferences
from src.restaurants.router import router as router_restaurants
from src.menu.router import router as router_menus

from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title='JAMIK'
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS Setup
origins = [
    "http://localhost:4200",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/auth/jwt", 
    tags=["auth"]
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_user)):
    return {"message": f"Hello {user.email}!"}


app.include_router(router_preferences)


app.include_router(router_restaurants)


app.include_router(router_menus)

