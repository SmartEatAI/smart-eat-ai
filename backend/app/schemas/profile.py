from pydantic import BaseModel, Field, field_validator
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

class DietTypeEnum(str, Enum):
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
    goal: GoalEnum = Field(..., description="User's fitness goal")
    height: float = Field(..., gte=140, lte=220, description="User's height in cm")
    weight: float = Field(..., gte=35, lte=300, description="User's weight in kg")
    body_type: BodyTypeEnum = Field(..., description="User's body type")
    gender: GenderEnum = Field(..., description="User's gender")
    meals_per_day: int = Field(..., gte=1, lte=6, description="Number of meals per day")
    activity_level: ActivityLevelEnum = Field(..., description="User's activity level")
    birth_date: date = Field(..., description="User's birth date")
    
    @field_validator("birth_date")
    @classmethod
    def validate_age(cls, value):
        today = date.today()
        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )

        if age < 16:
            raise ValueError("User must be at least 16 years old")
        if age > 100:
            raise ValueError("User must be less than or equal to 100 years old")

        return value
    
    body_fat_percentage: Optional[float] = Field(default=0.0, gte=0.0, description="User's body fat percentage")
    calories_target: Optional[float] = Field(default=0.0, gte=0.0, description="User's target calories")
    protein_target: Optional[float] = Field(default=0.0, gte=0.0, description="User's target protein in grams")
    carbs_target: Optional[float] = Field(default=0.0, gte=0.0, description="User's target carbs in grams")
    fat_target: Optional[float] = Field(default=0.0, gte=0.0, description="User's target fat in grams")

class ProfileCreate(ProfileBase):
    tastes: Optional[List[CategoryUpdate]] = []
    restrictions: Optional[List[CategoryUpdate]] = []
    diet_types: Optional[List[DietTypeEnum]] = []

class ProfileUpdate(ProfileBase):
    tastes: Optional[List[CategoryUpdate]] = []
    restrictions: Optional[List[CategoryUpdate]] = []
    diet_types: Optional[List[DietTypeEnum]] = []

class ProfileResponse(ProfileBase):
    id: int = Field(..., description="Profile ID")
    user_id: int = Field(..., description="Associated User ID")
    tastes: List[CategoryResponse] = []
    restrictions: List[CategoryResponse] = []
    diet_types: List[CategoryResponse] = []

    class Config:
        from_attributes = True