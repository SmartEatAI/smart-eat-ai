from pydantic import BaseModel
from typing import List, Optional
from datetime import time
from enum import Enum

class MealTypeEnum(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"

class MealDetailBase(BaseModel):
    recipe_id: int
    schedule: Optional[time] = None
    status: Optional[int] = 0
    meal_type: MealTypeEnum

class MealDetailResponse(MealDetailBase):
    id: int
    recipe: RecipeResponse # Esto permite ver los datos de la receta en el menú

    class Config:
        from_attributes = True

class DailyMenuBase(BaseModel):
    day_of_week: int # 1-7 (Lunes-Domingo)

class DailyMenuResponse(DailyMenuBase):
    id: int
    meal_details: List[MealDetailResponse] = []

    class Config:
        from_attributes = True