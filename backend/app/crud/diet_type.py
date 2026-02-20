from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.diet_type import DietType
from app.schemas.diet_type import DietTypeBase

def get_diet_types(db: Session):
  """Obtiene todos los tipos de comida de la base de datos."""
  try:
    return db.query(DietType).all()
  except Exception as e:
    print(f"Error al obtener tipos de comida: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar los tipos de comida en la base de datos"
    )

def get_diet_type_by_id(db: Session, diet_type_id: int):
  """"Obtiene un tipo de comida por su ID."""
  try:
    return db.query(DietType).filter(DietType.id == diet_type_id).first()
  except Exception as e:
    print(f"Error al obtener tipo de comida por ID: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar los tipos de comida en la base de datos"
    )

def get_recipes_by_diet_type(db: Session, diet_type: str):
  """Obtiene las recetas por su tipo de comida."""
  try:
    return db.query(DietType).filter(DietType.name == diet_type).first().recipes
  except Exception as e:
    print(f"Error al obtener recetas por tipo de comida: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar las recetas en la base de datos"
    )