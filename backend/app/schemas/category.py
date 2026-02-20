from pydantic import BaseModel, field_validator

# Esquema aplicable a MealType, DietType, Taste y Restriction
# ya que comparten el mismo formato de datos
class CategoryBase(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def to_lowercase(cls, v: str) -> str:
        return v.strip().lower()

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True
