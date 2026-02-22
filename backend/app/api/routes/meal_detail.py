from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.meal_detail import MealDetailBase, MealDetailResponse
from app.crud import meal_detail as crud

router = APIRouter(prefix="/meal-detail")
@router.get("/{meal_detail_id}", response_model=MealDetailResponse)
def get_meal_detail_by_id(
    meal_detail_id: int, 
    db: Session = Depends(get_db)
):
    meal_detail = crud.get_meal_details_by_id(db, meal_detail_id=meal_detail_id)
    if not meal_detail:
        raise HTTPException(status_code=404, detail="Detalle de comida no encontrado")
    return meal_detail
  
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