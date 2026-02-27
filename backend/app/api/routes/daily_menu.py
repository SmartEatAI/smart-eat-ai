from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.daily_menu import DailyMenuCreate, DailyMenuResponse
from app.services.daily_menu import DailyMenuService

router = APIRouter(prefix="/daily-menu")

@router.get("/{daily_menu_id}", response_model=DailyMenuResponse)
def get_daily_menu_by_id(
    daily_menu_id: int, 
    db: Session = Depends(get_db)
):
    return DailyMenuService.get_daily_menu_by_id(db, daily_menu_id=daily_menu_id)

@router.post("/", response_model=DailyMenuResponse)
def create_daily_menu(
    daily_menu_in: DailyMenuCreate, 
    db: Session = Depends(get_db)
):
    return DailyMenuService.create_daily_menu(db, obj_in=daily_menu_in)