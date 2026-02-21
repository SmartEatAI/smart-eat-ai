from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.meal_type import MealTypeBase, MealTypeResponse
from app.crud import meal_type as crud

router = APIRouter(prefix="/meal-types", tags=["Meal Types"])
@router.get("/", response_model=list[MealTypeResponse])
def get_meal_types(db: Session = Depends(get_db)):
  """Obtiene todos los tipos de comida."""
  return crud.get_meal_types(db)

@router.get("/{meal_type_id}", response_model=MealTypeResponse)
def get_meal_type_by_id(meal_type_id: int, db: Session = Depends(get_db)):
  """Obtiene un tipo de comida por su ID."""
  meal_type = crud.get_meal_type_by_id(db, meal_type_id)
  if not meal_type:
    raise HTTPException(status_code=404, detail="Tipo de comida no encontrado")
  return meal_type

@router.get("/{meal_type}/recipes", response_model=list[MealTypeResponse])
def get_recipes_by_meal_type(meal_type: str, db: Session = Depends(get_db)):
  """Obtiene las recetas por su tipo de comida."""
  recipes = crud.get_recipes_by_meal_type(db, meal_type)
  if not recipes:
    raise HTTPException(status_code=404, detail="Recetas no encontradas para este tipo de comida")
  return recipes