from enum import Enum
from datetime import time
from typing import Optional
from pydantic import BaseModel

from .recipe import RecipeResponse
from .daily_menu import DailyMenuResponse

# Definicion de Enums para que Pydantic valide los strings permitidos
class MealTypeEnum(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"


# Esquemas para Detalles de Comida dentro del Menú Diario
class MealDetailBase(BaseModel):
    recipe_id: int
    daily_menu_id: int
    schedule: Optional[time] = None
    status: Optional[int] = 0
    meal_type: MealTypeEnum

# Esquema para la respuesta de MealDetail
class MealDetailResponse(MealDetailBase):
    id: int
    recipe: RecipeResponse # Esto permite ver los datos de la receta en el menú
    daily_menu: Optional[DailyMenuResponse] = None # # Relación opcional con el menú diario
    class Config:
        from_attributes = True

