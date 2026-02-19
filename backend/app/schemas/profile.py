from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from decimal import Decimal
from enum import Enum

from backend.app.schemas.profile_eating_style import EatingStyleEnum, ProfileEatingStyleResponse
from backend.app.schemas.taste import TasteResponse


# Definicion de Enums para que Pydantic valide los strings permitidos
class GoalEnum(str, Enum):
    lose_weight = "lose_weight"
    maintain_weight = "maintain_weight"
    gain_weight = "gain_weight"

class ActivityLevelEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

# Esquemas para Restricciones
class RestrictionBase(BaseModel):
    name: str

class RestrictionResponse(RestrictionBase):
    id: int
    class Config:
        from_attributes = True


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
    #### pasar ids o objetos completos? #### REVISAR
    taste_ids: Optional[List[int]] = []
    restriction_ids: Optional[List[int]] = []
    eating_styles: Optional[List[EatingStyleEnum]] = []

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    tastes: List[TasteResponse] = []
    restrictions: List[RestrictionResponse] = []
    eating_styles: List[ProfileEatingStyleResponse] = []

    class Config:
        from_attributes = True