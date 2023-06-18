from pydantic import BaseModel


class AddRating(BaseModel):
    id_food: int
    id_user: int
    rating: int