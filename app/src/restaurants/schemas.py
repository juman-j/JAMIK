from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    id: int
    name: str
    phone_number: str
    email: str
    
    