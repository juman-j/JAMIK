from pydantic import BaseModel


class PreferenceCreate(BaseModel):
    user_id: int
    preferred_cuisine: list
    preferred_ingredients: list
    disliked_ingredients: list
    allergens: list
    nutritional_preferences: list