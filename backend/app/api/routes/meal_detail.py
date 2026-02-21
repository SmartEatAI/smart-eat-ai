from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.meal_detail import MealDetailBase, MealDetailResponse
from app.crud import meal_detail as crud

router = APIRouter(prefix="/meal-detail", tags=["Meal Detail"])
@router.get("/{meal_detail_id}", response_model=MealDetailResponse)
def get_meal_detail_by_id(
    meal_detail_id: int, 
    db: Session = Depends(get_db)
):
    return crud.get_meal_details_by_id(db, meal_detail_id=meal_detail_id)
  
@router.get("/daily-menu/{daily_menu_id}", response_model=list[MealDetailResponse])
def get_meal_details_by_daily_menu_id(
    daily_menu_id: int, 
    db: Session = Depends(get_db)
):
    daily_menu =  crud.get_meal_details_by_daily_menu_id(db, daily_menu_id=daily_menu_id)
    if not daily_menu:
        raise HTTPException(status_code=404, detail="Detalles de comida no encontrados para el menú diario especificado")
    return daily_menu
  
@router.post("/", response_model=MealDetailResponse)
def create_meal_detail(
    meal_detail_in: MealDetailBase, 
    db: Session = Depends(get_db)
):
    return crud.create_meal_detail(db, obj_in=meal_detail_in)

@router.put("/{meal_detail_id}/status", response_model=MealDetailResponse)
def update_meal_detail_status(
    meal_detail_id: int, 
    status: int, 
    db: Session = Depends(get_db)
):
    return crud.update_meal_detail_status(db, meal_detail_id=meal_detail_id, status=status)
  
@router.put("/{meal_detail_id}", response_model=MealDetailResponse)
def update_meal_detail_recipe_id(
    meal_detail_id: int, 
    recipe_id: int, 
    db: Session = Depends(get_db)
):
    return crud.update_meal_detail_recipe_id(db, meal_detail_id=meal_detail_id, recipe_id=recipe_id)