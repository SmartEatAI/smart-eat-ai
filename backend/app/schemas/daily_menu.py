from pydantic import BaseModel
from typing import List, Optional
from datetime import time
from enum import Enum

from .meal_detail import MealDetailResponse

# Esquemas para Menú Diario
class DailyMenuBase(BaseModel):
    day_of_week: int # 1-7 (Lunes-Domingo)

class DailyMenuResponse(DailyMenuBase):
    id: int
    meal_details: List[MealDetailResponse] = []

    class Config:
        from_attributes = True