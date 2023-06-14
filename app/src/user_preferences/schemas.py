from pydantic import BaseModel


class PreferenceCreate(BaseModel):
    user_id: int
    preferred_ingredients: list
    allergens: list = None