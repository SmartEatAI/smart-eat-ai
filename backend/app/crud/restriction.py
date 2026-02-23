from app.schemas.category import CategoryBase
from sqlalchemy.orm import Session
from app.models.restriction import Restriction
from app.models.profile import Profile
from fastapi import HTTPException

def existing_restriction(db: Session, name: str):
    """Verifica si ya existe una restricción con el mismo nombre."""
    try:
        return db.query(Restriction).filter(Restriction.name == name.lower()).first()
    except Exception as e:
            print(f"Database error when existing_restriction: {e}")
            raise HTTPException(status_code=500, detail="Database error when existing_restriction")

def get_restrictions(db: Session):
    """Obtiene todas las restricciones de la base de datos."""
    try:
        return db.query(Restriction).all()
    except Exception as e:
        print(f"Database error when get_restrictions: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_restrictions")

def get_restriction_by_id(db: Session, restriction_id: int):
    """Obtiene una restricción por su ID."""
    try:
        return db.query(Restriction).filter(Restriction.id == restriction_id).first()
    except Exception as e:
        print(f"Database error when get_restriction_by_id: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_restriction_by_id")

def get_restrictions_by_profile(db: Session, profile_id: int):
    """Obtiene todas las restricciones asociadas a un perfil específico."""
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return []
        return profile.restrictions
    except Exception as e:
        print(f"Database error when get_restrictions_by_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_restrictions_by_profile")

def create_restriction_for_profile(db: Session, obj_in: CategoryBase, profile_id: int):
    """Crea una nueva restricción y la asocia a un perfil específico."""
    try:
        db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not db_profile:
            return None
        data = obj_in.model_dump()
        db_restriction = Restriction(**data)
        db_profile.restrictions.append(db_restriction)
        db.add(db_restriction)
        db.commit()
        db.refresh(db_restriction)
        return db_restriction
    except Exception as e:
        print(f"Database error when create_restriction_for_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when create_restriction_for_profile")

def add_restriction_to_profile(db: Session, restriction_id: int, profile_id: int):
    """Agrega una restricción existente a un perfil específico."""
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        restriction = db.query(Restriction).filter(Restriction.id == restriction_id).first()
        if not profile or not restriction:
            return None
        if restriction in profile.restrictions:
            return None
        profile.restrictions.append(restriction)
        db.commit()
        return restriction
    except Exception as e:
        print(f"Database error when add_restriction_to_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when add_restriction_to_profile")