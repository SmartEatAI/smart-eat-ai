from pydantic import BaseModel

# Esquema base para RecipeDietType
class RecipeDietTypeBase(BaseModel):
    recipe_id: int
    diet_type_id: int

# Esquema para la respuesta de RecipeDietType
class RecipeDietTypeResponse(RecipeDietTypeBase):
    class Config:
        from_attributes = True