from enum import Enum
from datetime import time
from typing import Optional
from pydantic import BaseModel, Field
from .recipe import RecipeResponse

# Definicion de Enums para que Pydantic valide los strings permitidos
class MealTypeEnum(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"


# Esquemas para Detalles de Comida dentro del Menú Diario
class MealDetailBase(BaseModel):
    recipe_id: int = Field(..., description="Recipe ID associated with the meal detail")
    daily_menu_id: int = Field(..., description="Daily Menu ID associated with the meal detail")
    schedule: int = Field(..., gte=1, lte=6, description="Schedule of the meal detail in minutes since midnight")
    status: int = Field(..., description="Status of the meal detail (0: pending, 1: completed)")
    meal_type: MealTypeEnum = Field(..., description="Type of meal (breakfast, lunch, dinner, snack)")

# Esquema para la respuesta de MealDetail
class MealDetailResponse(MealDetailBase):
    id: int = Field(..., description="ID of the meal detail")
    recipe: RecipeResponse = Field(..., description="Associated recipe details")
    class Config:
        from_attributes = True

