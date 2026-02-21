from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.diet_type import DietTypeBase, DietTypeResponse
from app.crud import diet_type as crud

router = APIRouter(prefix="/diet-type", tags=["Diet Type"])

@router.get("/", response_model=list[DietTypeResponse])
def get_diet_types(db: Session = Depends(get_db)):
  """Obtiene todos los tipos de comida."""
  return crud.get_diet_types(db)

@router.get("/{diet_type_id}", response_model=DietTypeResponse)
def get_diet_type_by_id(diet_type_id: int, db: Session = Depends(get_db)):
  """Obtiene un tipo de comida por su ID."""
  diet_type = crud.get_diet_type_by_id(db, diet_type_id=diet_type_id)
  if not diet_type:
    raise HTTPException(status_code=404, detail="Tipo de comida no encontrado")
  return diet_type

@router.get("/{diet_type}/recipes", response_model=list[DietTypeResponse])
def get_recipes_by_diet_type(diet_type: str, db: Session = Depends(get_db)):
  """Obtiene las recetas por su tipo de comida."""
  recipes = crud.get_recipes_by_diet_type(db, diet_type=diet_type)
  if not recipes:
    raise HTTPException(status_code=404, detail="Recetas no encontradas para este tipo de comida")
  return recipes