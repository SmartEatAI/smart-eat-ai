from app.schemas.category import CategoryBase
from app.crud.profile import get_profile
from sqlalchemy.orm import Session
from app.models.eating_style import EatingStyle
from app.models.profile import Profile

def existing_eating_style(db: Session, name: str):
    """Verifica si ya existe un estilo de alimentación con el mismo nombre."""
    return db.query(EatingStyle).filter(EatingStyle.name == name.lower()).first()

def get_eating_styles(db: Session):
    """Obtiene todas los estilos de alimentación de la base de datos."""
    return db.query(EatingStyle).all()

def get_eating_style_by_id(db: Session, eating_style_id: int):
    """"Obtiene un estilo de alimentación por su ID."""
    return db.query(EatingStyle).filter(EatingStyle.id == eating_style_id).first()

def get_eating_styles_by_profile(db: Session, profile_id: int):
    """Obtiene todos los estilos de alimentación asociados a un perfil específico."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        return []
    return profile.eating_styles

def create_eating_style_for_profile(db: Session, obj_in: CategoryBase, profile_id: int):
    """Crea un nuevo estilo de alimentación y lo asocia a un perfil específico."""
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        return None
    data = obj_in.model_dump()
    db_eating_style = EatingStyle(**data)
    db_profile.eating_styles.append(db_eating_style)
    db.add(db_eating_style)
    db.commit()
    db.refresh(db_eating_style)
    return db_eating_style

def add_eating_style_to_profile(db: Session, eating_style_id: int, profile_id: int):
    """Agrega un estilo de alimentación existente a un perfil específico."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    eating_style = db.query(EatingStyle).filter(EatingStyle.id == eating_style_id).first()
    if not profile or not eating_style:
        return None
    if eating_style in profile.eating_styles:
        return None
    profile.eating_styles.append(eating_style)
    db.commit()
    return eating_style

def create_eating_style(db: Session, obj_in: CategoryBase):
    """Crea un nuevo estilo de alimentación."""
    data = obj_in.model_dump()
    db_eating_style = EatingStyle(**data)
    db.add(db_eating_style)
    db.commit()
    db.refresh(db_eating_style)
    return db_eating_style