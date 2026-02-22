from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from enum import Enum
from .category import CategoryResponse, CategoryUpdate

# Definicion de Enums para que Pydantic valide los strings permitidos
class GoalEnum(str, Enum):
    lose_weight = "lose_weight"
    maintain_weight = "maintain_weight"
    gain_weight = "gain_weight"

class ActivityLevelEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class EatingStyleEnum(str, Enum):
    high_protein = "high_protein"
    low_carb = "low_carb"
    vegan = "vegan"
    vegetarian = "vegetarian"
    low_calorie = "low_calorie"
    high_fiber = "high_fiber"
    high_carb = "high_carb"

class BodyTypeEnum(str, Enum):
    lean = "lean"
    normal = "normal"
    stocky = "stocky"
    obese = "obese"

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

# Esquemas para Perfil
class ProfileBase(BaseModel):
    goal: GoalEnum
    height: float
    weight: float
    body_type: BodyTypeEnum
    gender: GenderEnum
    meals_per_day: int = Field(ge=1, le=20)
    activity_level: ActivityLevelEnum
    birth_date: date
    body_fat_percentage: Optional[float] = 0.0
    calories_target: Optional[float] = 0.0
    protein_target: Optional[float] = 0.0
    carbs_target: Optional[float] = 0.0
    fat_target: Optional[float] = 0.0

class ProfileCreate(ProfileBase):
    tastes: Optional[List[CategoryResponse]] = []
    restrictions: Optional[List[CategoryResponse]] = []
    eating_styles: Optional[List[EatingStyleEnum]] = []

class ProfileUpdate(ProfileBase):
    tastes: Optional[List[CategoryUpdate]] = []
    restrictions: Optional[List[CategoryUpdate]] = []
    eating_styles: Optional[List[EatingStyleEnum]] = []

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    tastes: List[CategoryResponse] = []
    restrictions: List[CategoryResponse] = []
    eating_styles: List[CategoryResponse] = []

    class Config:
        from_attributes = True