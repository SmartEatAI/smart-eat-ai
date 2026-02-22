from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .daily_menu import DailyMenuResponse

class PlanBase(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime] = None
    daily_menus: List[DailyMenuResponse] = []
    active: bool = True

class PlanCreate(PlanBase):
    user_id: int

class PlanResponse(PlanBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True