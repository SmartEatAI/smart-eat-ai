from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.taste import Taste
from app.models.restriction import Restriction
from app.schemas.profile import ProfileCreate, ProfileUpdate
from app.crud.category import process_profile_categories

def exist_profile(db: Session, user_id: int) -> bool:
    """Verifica si un perfil existe para un usuario específico."""
    return db.query(Profile).filter(Profile.user_id == user_id).first() is not None

def get_profile(db: Session, user_id: int) -> Profile:
    """Obtiene el perfil asociado a un usuario específico."""
    return db.query(Profile).filter(Profile.user_id == user_id).first()

def create_user_profile(db: Session, obj_in: ProfileCreate, user_id: int) -> Profile:
    """Crea un nuevo perfil para un usuario específico."""
    db_profile = Profile(**obj_in.model_dump(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_user_profile(db: Session, *, db_obj: Profile, obj_in: Dict[str, Any]) -> Profile:
    """
    Actualiza el perfil. 
    obj_in debe ser el diccionario de datos (puedes usar model_dump(exclude_unset=True)).
    """
    # Procesar Tastes
    if "tastes" in obj_in:
        db_obj.tastes = process_profile_categories(db, Taste, obj_in.pop("tastes"))

    # Procesar Restrictions
    if "restrictions" in obj_in:
        db_obj.restrictions = process_profile_categories(db, Restriction, obj_in.pop("restrictions"))

    # Actualizar campos directos
    for field, value in obj_in.items():
        if hasattr(db_obj, field):
            setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj