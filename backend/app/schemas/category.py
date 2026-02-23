from pydantic import BaseModel, field_validator, Field
from typing import Optional

# Esquema aplicable a MealType, DietType, Taste y Restriction
# ya que comparten el mismo formato de datos
class CategoryBase(BaseModel):
    name: str = Field(..., description="Name of the category")

    @field_validator('name')
    @classmethod
    def to_lowercase(cls, v: str) -> str:
        return v.strip().lower()
    
class CategoryUpdate(BaseModel):
    id: Optional[int] = Field(None, description="ID of the category to update")
    name: str = Field(..., description="Name of the category")

    @field_validator('name')
    @classmethod
    def to_lowercase(cls, v: str) -> str:
        return v.strip().lower()

class CategoryResponse(CategoryBase):
    id: int = Field(..., description="ID of the category")
    class Config:
        from_attributes = True
