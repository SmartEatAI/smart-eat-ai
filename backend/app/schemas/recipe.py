from pydantic import BaseModel, Field
from typing import List, Optional
from .category import CategoryResponse, CategoryBase

# Esquema para la receta
class RecipeBase(BaseModel):
    name: str = Field(..., example="Spaghetti Carbonara")
    calories: int = Field(..., example=400)
    protein: int = Field(..., example=20)
    carbs: int = Field(..., example=50)
    fat: int = Field(..., example=15)
    image_url: Optional[str] = Field(default=None, example="https://example.com/image.jpg")
    recipe_url: Optional[str] = Field(default=None, example="https://example.com/recipe")

class RecipeCreate(RecipeBase):
    meal_types: List[CategoryBase] = []
    diet_types: List[CategoryBase] = []

class RecipeResponse(RecipeBase):
    id: int = Field(..., example=1)
    meal_types: List[CategoryResponse] = []
    diet_types: List[CategoryResponse] = []
    
    class Config:
        from_attributes = True