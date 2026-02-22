from sqlalchemy.orm import Session
from app.models.profile import Profile

def exist_profile(db: Session, user_id: int) -> bool:
    """Verifica si un perfil existe para un usuario específico."""
    return db.query(Profile).filter(Profile.user_id == user_id).first() is not None

def get_profile(db: Session, user_id: int) -> Profile:
    """Obtiene el perfil asociado a un usuario específico."""
    return db.query(Profile).filter(Profile.user_id == user_id).first()

def create_profile(db: Session, profile_dict: dict, user_id: int) -> Profile:
    """Crea un nuevo perfil de usuario."""
    new_profile = Profile(**profile_dict, user_id=user_id)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

def update_profile(db: Session, db_profile: Profile, profile_dict: dict) -> Profile:
    """Actualiza un perfil de usuario existente."""
    for field, value in profile_dict.items():
        setattr(db_profile, field, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile