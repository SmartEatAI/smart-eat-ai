from sqlalchemy.orm import Session
from app.models.diet_type import DietType

def get_diet_types(db: Session):
  """Obtiene todas los tipos de dieta de la base de datos."""
  return db.query(DietType).all()

def get_diet_type_by_id(db: Session, diet_type_id: int):
  """Obtiene un tipo de dieta por su ID."""
  return db.query(DietType).filter(DietType.id == diet_type_id).first()