from sqlalchemy.orm import Session
from app.models.meal_type import MealType

def get_meal_types(db: Session):
  """Obtiene todas los tipos de comida de la base de datos."""
  return db.query(MealType).all()

def get_meal_type_by_id(db: Session, meal_type_id: int):
  """Obtiene un tipo de comida por su ID."""
  return db.query(MealType).filter(MealType.id == meal_type_id).first()