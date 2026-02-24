from sqlalchemy.orm import Session
from app.models.profile import Profile
from fastapi import HTTPException

def exist_profile(db: Session, user_id: int) -> bool:
    """Verifica si un perfil existe para un usuario específico."""
    try:
        return db.query(Profile).filter(Profile.user_id == user_id).first() is not None
    except Exception as e:
        print(f"Database error when exist_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when exist_profile")

def get_profile(db: Session, user_id: int) -> Profile:
    """Obtiene el perfil asociado a un usuario específico."""
    try:
        return db.query(Profile).filter(Profile.user_id == user_id).first()
    except Exception as e:
        print(f"Database error when get_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_profile")

def create_profile(db: Session, profile_dict: dict, user_id: int) -> Profile:
    """Crea un nuevo perfil de usuario."""
    try:
        new_profile = Profile(**profile_dict, user_id=user_id)
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile
    except Exception as e:
        print(f"Database error when create_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when create_profile")

def update_profile(db: Session, db_profile: Profile, profile_dict: dict) -> Profile:
    """Actualiza un perfil de usuario existente."""
    try:
        for field, value in profile_dict.items():
            setattr(db_profile, field, value)
        db.commit()
        db.refresh(db_profile)
        return db_profile
    except Exception as e:
        print(f"Database error when update_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when update_profile")