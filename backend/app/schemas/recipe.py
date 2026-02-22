from pydantic import BaseModel
from typing import List, Optional
from .category import CategoryResponse

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