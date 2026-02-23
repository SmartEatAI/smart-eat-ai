from sqlalchemy.orm import Session
from app.models.taste import Taste
from app.models.profile import Profile
from app.schemas.category import CategoryBase
from fastapi import HTTPException

def existing_taste(db: Session, name: str):
    """Verifica si ya existe un gusto con el mismo nombre."""
    try:
        return db.query(Taste).filter(Taste.name == name.lower()).first()
    except Exception as e:
        print(f"Database error when existing_taste: {e}")
        raise HTTPException(status_code=500, detail="Database error when existing_taste")

def get_tastes(db: Session):
    """Obtiene todas los gustos de la base de datos."""
    try:
        return db.query(Taste).all()
    except Exception as e:
        print(f"Database error when get_tastes: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_tastes")

def get_taste_by_id(db: Session, taste_id: int):
    """Obtiene un gusto por su ID."""
    try:
        return db.query(Taste).filter(Taste.id == taste_id).first()
    except Exception as e:
        print(f"Database error when get_taste_by_id: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_taste_by_id")

def get_tastes_by_profile(db: Session, profile_id: int):
    """Obtiene todos los gustos asociados a un perfil específico."""
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return []
        return profile.tastes
    except Exception as e:
        print(f"Database error when get_tastes_by_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_tastes_by_profile")

def create_taste_for_profile(db: Session, obj_in: CategoryBase, profile_id: int):
    """Crea un nuevo gusto y lo asocia a un perfil específico."""
    try:
        db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not db_profile:
            return None
        data = obj_in.model_dump()
        db_taste = Taste(**data)
        db_profile.tastes.append(db_taste)
        db.add(db_taste)
        db.commit()
        db.refresh(db_taste)
        return db_taste
    except Exception as e:
        print(f"Database error when create_taste_for_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when create_taste_for_profile")         

def add_taste_to_profile(db: Session, taste_id: int, profile_id: int):
    """Agrega un gusto existente a un perfil específico."""
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        taste = db.query(Taste).filter(Taste.id == taste_id).first()
        if not profile or not taste:
            return None
        if taste in profile.tastes:
            return None
        profile.tastes.append(taste)
        db.commit()
        return taste
    except Exception as e:
        print(f"Database error when add_taste_to_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when add_taste_to_profile")