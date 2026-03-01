from app.schemas.enums import MealTypeEnum
from pydantic import BaseModel, Field
from .recipe import RecipeResponse

# Esquemas para Detalles de Comida dentro del Menú Diario
class MealDetailBase(BaseModel):
    recipe_id: int = Field(..., description="Recipe ID associated with the meal detail")
    # Este campo no es necesario
    #daily_menu_id: int = Field(..., description="Daily Menu ID associated with the meal detail")
    schedule: int = Field(..., gte=1, lte=6, description="Order meals (1-6)")
    status: int = Field(..., description="Status of the meal detail (0: pending, 1: completed)")
    meal_type: MealTypeEnum = Field(..., description="Type of meal (breakfast, lunch, dinner, snack)")

class MealDetailCreate(MealDetailBase):
    daily_menu_id: int = Field(..., description="Daily Menu ID associated with the meal detail")

# Esquema para la respuesta de MealDetail
class MealDetailResponse(MealDetailBase):
    id: int = Field(..., description="ID of the meal detail")
    recipe: RecipeResponse = Field(..., description="Associated recipe details")
    class Config:
        from_attributes = True

