from pydantic import BaseModel


class PreferenceCreate(BaseModel):
    user_id: int
    preferred_ingredients: list
    diet_restriction: list = None
    metric_system: str
    allergens: list = None

