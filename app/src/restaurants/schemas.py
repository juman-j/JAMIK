from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    phone_number: str
    email: str
    
    