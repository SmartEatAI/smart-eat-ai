from pydantic import BaseModel, Field
from typing import List

from .meal_detail import MealDetailResponse

# Esquemas para Menú Diario
class DailyMenuBase(BaseModel):
    plan_id: int = Field(..., description="Plan ID to which this daily menu belongs")
    day_of_week: int = Field(..., gte=1, lte=7, description="Day of the week (1-7, where 1 is Monday)")

class DailyMenuResponse(DailyMenuBase):
    id: int = Field(..., description="Unique identifier for the daily menu")
    meal_details: List[MealDetailResponse] = []

    class Config:
        from_attributes = True