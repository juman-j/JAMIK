from fastapi import Depends, FastAPI
from models.models import User
from auth.base_config import auth_backend, fastapi_users, current_user
from auth.schemas import UserCreate, UserRead

from user_preferences.router import router as router_preferences


app = FastAPI(
    title='JAMIK'
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