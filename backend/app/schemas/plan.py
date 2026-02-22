from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from .daily_menu import DailyMenuResponse

class PlanBase(BaseModel):
    created_at: datetime = Field(..., description="The timestamp when the plan was created")
    updated_at: datetime = Field(..., description="The timestamp when the plan was last updated")
    daily_menus: List[DailyMenuResponse] = []
    active: bool = Field(..., description="Indicates whether the plan is active")

class PlanCreate(PlanBase):
    user_id: int = Field(..., description="The ID of the user to whom the plan belongs")

class PlanResponse(PlanBase):
    id: int = Field(..., description="The unique identifier of the plan")
    user_id: int = Field(..., description="The ID of the user to whom the plan belongs")
    class Config:
        from_attributes = True