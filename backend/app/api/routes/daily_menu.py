from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.daily_menu import DailyMenuBase, DailyMenuResponse
from app.crud import daily_menu as crud
from app.models import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/daily-menu", tags=["Daily Menu"])

@router.get("/{daily_menu_id}", response_model=list[DailyMenuResponse])
def get_daily_menu_by_id(
    daily_menu_id: int, 
    db: Session = Depends(get_db)
):
    return crud.get_daily_menu_by_id(db, daily_menu_id=daily_menu_id)

@router.get("/plan/{plan_id}", response_model=list[DailyMenuResponse])
def get_daily_menus(
  plan_id: int,
  db: Session = Depends(get_db)
):
    return crud.get_daily_menu_by_plan_id(db, plan_id=plan_id)

@router.post("/", response_model=DailyMenuResponse)
def create_daily_menu(
    daily_menu_in: DailyMenuBase, 
    db: Session = Depends(get_db)
):
    return crud.create_daily_menu(db, obj_in=daily_menu_in)