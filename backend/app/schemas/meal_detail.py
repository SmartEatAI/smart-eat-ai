from enum import Enum
from datetime import time
from typing import Optional
from pydantic import BaseModel

from .recipe import RecipeResponse

# Definicion de Enums para que Pydantic valide los strings permitidos
class MealTypeEnum(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"


# Esquemas para Detalles de Comida dentro del Menú Diario
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

