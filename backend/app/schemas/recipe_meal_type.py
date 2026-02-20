from pydantic import BaseModel

# Esquema base para RecipeMealType
class RecipeMealTypeBase(BaseModel):
    recipe_id: int
    meal_type_id: int

# Esquema para la respuesta de RecipeMealType
class RecipeMealTypeResponse(RecipeMealTypeBase):
    class Config:
        from_attributes = True