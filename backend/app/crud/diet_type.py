from sqlalchemy.orm import Session
from app.models.diet_type import DietType
from fastapi import HTTPException

def get_diet_types(db: Session):
  """Obtiene todas los tipos de dieta de la base de datos."""
  try:
    return db.query(DietType).all()
  except Exception as e:
        print(f"Database error when get_diet_types: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_diet_types")

def get_diet_type_by_id(db: Session, diet_type_id: int):
  """Obtiene un tipo de dieta por su ID."""
  try:
    return db.query(DietType).filter(DietType.id == diet_type_id).first()
  except Exception as e:
        print(f"Database error when get_diet_type_by_id: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_diet_type_by_id")