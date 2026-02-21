from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.meal_detail import MealDetailBase, MealDetailResponse
from app.crud import meal_detail as crud
from app.models import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/daily-menu", tags=["Daily Menu"])

@router.get("/{daily_menu_id}", response_model=list[MealDetailResponse])
def get_daily_menu_by_id(
    daily_menu_id: int, 
    db: Session = Depends(get_db)
):
    return crud.get_daily_menu_by_id(db, daily_menu_id=daily_menu_id)

@router.get("/plan/{plan_id}", response_model=list[MealDetailResponse])
def get_daily_menus(
  plan_id: int,
  db: Session = Depends(get_db)
):
    return crud.get_daily_menu_by_plan_id(db, plan_id=plan_id)

@router.post("/", response_model=MealDetailResponse)
def create_daily_menu(
    meal_detail_in: MealDetailBase, 
    db: Session = Depends(get_db)
):
    return crud.create_daily_menu(db, obj_in=meal_detail_in)