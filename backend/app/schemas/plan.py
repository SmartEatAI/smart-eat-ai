from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from .daily_menu import DailyMenuCreate, DailyMenuResponse

class PlanBase(BaseModel):
    #created_at: datetime = Field(..., description="The timestamp when the plan was created")
    #updated_at: datetime = Field(..., description="The timestamp when the plan was last updated")
    #daily_menus: List[DailyMenuResponse] = []
    #active: bool = Field(..., description="Indicates whether the plan is active")
    pass

class PlanCreate(PlanBase):
    #user_id: int = Field(..., description="The ID of the user to whom the plan belongs")
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