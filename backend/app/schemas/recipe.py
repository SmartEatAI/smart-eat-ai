from pydantic import BaseModel, HttpUrl
from typing import List, Optional

# Esquema aplicable a MealType y DietType, ya que ambos comparten el mismo formato de datos
class CategoryBase(BaseModel):
    name: str

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# Esquema para la receta
class RecipeBase(BaseModel):
    name: str
    calories: int
    protein: int
    carbs: int
    fat: int
    image_url: Optional[str] = None
    recipe_url: Optional[str] = None

class RecipeResponse(RecipeBase):
    id: int
    meal_types: List[CategoryResponse] = []
    diet_types: List[CategoryResponse] = []
    
    class Config:
        from_attributes = True