from app.schemas.category import CategoryBase
from sqlalchemy.orm import Session
from app.models.diet_type import DietType

def get_diet_types(db: Session):
  """Obtiene todas los tipos de dieta de la base de datos."""
  return db.query(DietType).all()

def get_diet_type_by_id(db: Session, diet_type_id: int):
  """Obtiene un tipo de dieta por su ID."""
  return db.query(DietType).filter(DietType.id == diet_type_id).first()

def get_diet_types_by_name(db: Session, name: str):
    """Obtiene tipos de dieta por una lista de nombres."""
    return db.query(DietType).filter(DietType.name == name).first()

def existing_diet_type(db: Session, name: str):
    """Verifica si ya existe un tipo de dieta con el mismo nombre."""
    return db.query(DietType).filter(DietType.name == name.lower()).first()

def create_diet_type(db: Session, obj_in: CategoryBase):
    """Crea un nuevo tipo de dieta."""
    data = obj_in.model_dump()
    db_diet_type = DietType(**data)
    db.add(db_diet_type)
    db.commit()
    db.refresh(db_diet_type)
    return db_diet_type