from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware

from src.models.models import User
from src.auth.schemas import UserRead
from src.auth.schemas import UserCreate
from src.auth.base_config import auth_backend
from src.auth.base_config import fastapi_users
from src.auth.base_config import current_user

from src.menu.router import router as router_menus
from src.restaurants.router import router as router_restaurants
from src.user_preferences.router import router as router_preferences


app = FastAPI(
    title='JAMIK'
)


# CORS Setup
origins = [
    "http://localhost:4200",
    "https://648e38c39ea3325336d1a319--incredible-stardust-814e38.netlify.app"
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

