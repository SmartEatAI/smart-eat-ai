from pydantic import BaseModel

# Esquema aplicable a MealType, DietType, Taste y Restriction
# ya que comparten el mismo formato de datos
class CategoryBase(BaseModel):
    name: str

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True
