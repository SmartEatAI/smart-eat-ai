from enum import Enum
from pydantic import BaseModel

class EatingStyleEnum(str, Enum):
    high_protein = "high_protein"
    low_carb = "low_carb"
    vegan = "vegan"
    vegetarian = "vegetarian"
    low_calorie = "low_calorie"
    high_fiber = "high_fiber"
    high_carb = "high_carb"

# Esquema para Estilos de Alimentación
class ProfileEatingStyleBase(BaseModel):
    name: EatingStyleEnum

class ProfileEatingStyleResponse(ProfileEatingStyleBase):
    id: int
    
    class Config:
        from_attributes = True
