from sqlalchemy.orm import Session
from app.models.meal_type import MealType
from fastapi import HTTPException

def get_meal_types(db: Session):
  """Obtiene todas los tipos de comida de la base de datos."""
  try:
    return db.query(MealType).all()
  except Exception as e:
        print(f"Database error when get_meal_types: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_meal_types")

def get_meal_type_by_id(db: Session, meal_type_id: int):
  """Obtiene un tipo de comida por su ID."""
  try:
    return db.query(MealType).filter(MealType.id == meal_type_id).first()
  except Exception as e:
        print(f"Database error when get_meal_type_by_id: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_meal_type_by_id")