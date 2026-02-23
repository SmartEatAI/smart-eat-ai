from sqlalchemy.orm import Session
from app.models.meal_type import MealType

def get_meal_types(db: Session):
  """Obtiene todas los tipos de comida de la base de datos."""
  return db.query(MealType).all()

def get_meal_type_by_id(db: Session, meal_type_id: int):
  """Obtiene un tipo de comida por su ID."""
  return db.query(MealType).filter(MealType.id == meal_type_id).first()

def get_meal_types_by_name(db: Session, name: str):
    """Obtiene tipos de comida por una lista de nombres."""
    return db.query(MealType).filter(MealType.name == name).first()

def existing_meal_type(db: Session, name: str):
  """Verifica si un tipo de comida con el mismo nombre ya existe."""
  return db.query(MealType).filter(MealType.name == name).first()

def create_meal_type(db: Session, meal_type_schema):
  """Crea un nuevo tipo de comida en la base de datos."""
  meal_type = MealType(name=meal_type_schema.name)
  db.add(meal_type)
  db.commit()
  db.refresh(meal_type)
  return meal_type