from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.meal_type import MealType

def get_meal_types(db: Session):
  """Obtiene todos los tipos de comida de la base de datos."""
  try:
    return db.query(MealType).all()
  except Exception as e:
    print(f"Error al obtener tipos de comida: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar los tipos de comida en la base de datos"
    )

def get_meal_type_by_id(db: Session, meal_type_id: int):
  """"Obtiene un tipo de comida por su ID."""
  try:
    return db.query(MealType).filter(MealType.id == meal_type_id).first()
  except Exception as e:
    print(f"Error al obtener tipo de comida por ID: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar los tipos de comida en la base de datos"
    )