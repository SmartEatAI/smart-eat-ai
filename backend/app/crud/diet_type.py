from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.diet_type import DietType

def get_diet_types(db: Session):
  """Obtiene todos los tipos de dieta de la base de datos."""
  try:
    return db.query(DietType).all()
  except Exception as e:
    print(f"Error al obtener tipos de dieta: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar los tipos de dieta en la base de datos"
    )

def get_diet_type_by_id(db: Session, diet_type_id: int):
  """"Obtiene un tipo de dieta por su ID."""
  try:
    return db.query(DietType).filter(DietType.id == diet_type_id).first()
  except Exception as e:
    print(f"Error al obtener tipo de dieta por ID: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar los tipos de dieta en la base de datos"
    )
