from app.schemas.category import CategoryBase
from app.crud.profile import get_profile
from sqlalchemy.orm import Session
from app.models.diet_type import DietType
from app.models.profile import Profile
from fastapi import HTTPException

def existing_diet_type(db: Session, name: str):
    """Verifica si ya existe un estilo de alimentación con el mismo nombre."""
    try:
        return db.query(DietType).filter(DietType.name == name.lower()).first()
    except Exception as e:
        print(f"Database error when existing_diet_type: {e}")
        raise HTTPException(status_code=500, detail="Database error when existing_diet_type")

def get_diet_types(db: Session):
    """Obtiene todas los estilos de alimentación de la base de datos."""
    try:
        return db.query(DietType).all()
    except Exception as e:
        print(f"Database error when get_diet_types: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_diet_types")

def get_diet_type_by_id(db: Session, diet_type_id: int):
    """"Obtiene un estilo de alimentación por su ID."""
    try:
        return db.query(DietType).filter(DietType.id == diet_type_id).first()
    except Exception as e:
        print(f"Database error when get_diet_type_by_id: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_diet_type_by_id")

def get_diet_types_by_profile(db: Session, profile_id: int):
    """Obtiene todos los estilos de alimentación asociados a un perfil específico."""
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return []
        return profile.diet_types
    except Exception as e:
        print(f"Database error when get_diet_types_by_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_diet_types_by_profile")

def create_diet_type_for_profile(db: Session, obj_in: CategoryBase, profile_id: int):
    """Crea un nuevo estilo de alimentación y lo asocia a un perfil específico."""
    try:
        db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not db_profile:
            return None
        data = obj_in.model_dump()
        db_diet_type = DietType(**data)
        db_profile.diet_types.append(db_diet_type)
        db.add(db_diet_type)
        db.commit()
        db.refresh(db_diet_type)
        return db_diet_type
    except Exception as e:
        print(f"Database error when create_diet_type_for_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when create_diet_type_for_profile")

def add_diet_type_to_profile(db: Session, diet_type_id: int, profile_id: int):
    """Agrega un estilo de alimentación existente a un perfil específico."""
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        diet_type = db.query(DietType).filter(DietType.id == diet_type_id).first()
        if not profile or not diet_type:
            return None
        if diet_type in profile.diet_types:
            return None
        profile.diet_types.append(diet_type)
        db.commit()
        return diet_type
    except Exception as e:
        print(f"Database error when add_diet_type_to_profile: {e}")
        raise HTTPException(status_code=500, detail="Database error when add_diet_type_to_profile")