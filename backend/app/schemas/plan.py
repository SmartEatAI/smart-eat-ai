from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from .daily_menu import DailyMenuCreate, DailyMenuResponse

class PlanBase(BaseModel):
    pass

class PlanCreate(PlanBase):
    daily_menus: List[DailyMenuCreate] = []

class PlanResponse(PlanBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    daily_menus: List[DailyMenuResponse] = []
    active: bool = Field(..., description="Indicates whether the plan is active")
    class Config:
        from_attributes = True