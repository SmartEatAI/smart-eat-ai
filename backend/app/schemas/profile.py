from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from decimal import Decimal
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

# Esquemas para Perfil
class ProfileBase(BaseModel):
    goal: Optional[GoalEnum] = None
    height: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    body_fat_percentage: Optional[int] = Field(None, ge=0, le=100)
    calories_target: Optional[int] = None
    protein_target: Optional[int] = None
    carbs_target: Optional[int] = None
    fat_target: Optional[int] = None
    gender: Optional[str] = None
    meals_per_day: Optional[int] = Field(None, ge=1, le=20)
    activity_level: Optional[ActivityLevelEnum] = None
    birth_date: Optional[date] = None

class ProfileCreate(ProfileBase):
    tastes: Optional[List[CategoryResponse]] = []
    restrictions: Optional[List[CategoryResponse]] = []
    eating_styles: Optional[List[EatingStyleEnum]] = []

class ProfileUpdate(ProfileBase):
    tastes: Optional[List[CategoryUpdate]] = None
    restrictions: Optional[List[CategoryUpdate]] = None
    eating_styles: Optional[List[EatingStyleEnum]] = None

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    tastes: List[CategoryResponse] = []
    restrictions: List[CategoryResponse] = []
    eating_styles: List[EatingStyleEnum] = []

    class Config:
        from_attributes = True