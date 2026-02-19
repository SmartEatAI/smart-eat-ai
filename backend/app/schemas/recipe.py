from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True

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