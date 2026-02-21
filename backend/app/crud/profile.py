from http.client import HTTPException
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.taste import Taste
from app.models.restriction import Restriction
from app.schemas.profile import ProfileCreate, ProfileUpdate
from app.crud.category import process_profile_categories

def exist_profile(db: Session, user_id: int) -> bool:
    """Verifica si un perfil existe para un usuario específico."""
    try:
        return db.query(Profile).filter(Profile.user_id == user_id).first() is not None
    except Exception as e:
        print(f"Error al verificar si existe el perfil: {e}")
        raise e

def get_profile(db: Session, user_id: int):
    """Obtiene el perfil asociado a un usuario específico."""
    return db.query(Profile).filter(Profile.user_id == user_id).first()

def create_user_profile(db: Session, obj_in: ProfileCreate, user_id: int):
    """Crea un nuevo perfil para un usuario específico."""
    try:
        db_profile = Profile(**obj_in.model_dump(), user_id=user_id)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile
    except Exception as e:
        db.rollback()
        print(f"Error al crear el perfil: {e}")
        raise e

def update_user_profile(db: Session, *, db_obj: Profile, obj_in: Dict[str, Any]) -> Profile:
    """
    Actualiza el perfil. 
    obj_in debe ser el diccionario de datos (puedes usar model_dump(exclude_unset=True)).
    """
    try:
        # Procesar Tastes
        if "tastes" in obj_in:
            db_obj.tastes = process_profile_categories(db, Taste, obj_in.pop("tastes"))

        # Procesar Restrictions
        if "restrictions" in obj_in:
            db_obj.restrictions = process_profile_categories(db, Restriction, obj_in.pop("restrictions"))

        # Actualizar campos directos y Enums (goal, eating_styles, etc.)
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    except Exception as e:
        db.rollback()
        print(f"Error en update_user_profile: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el perfil")

def update_profile_macros(
    db: Session,
    user_id: int,
    calories: int,
    protein: int,
    fat: int,
    carbs: int
):
    try:
        db_obj = get_profile(db, user_id)
        
        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"No hay perfil para el usuario con id {user_id}"
            )
        
        db_obj.calories_target = calories
        db_obj.protein_target = protein
        db_obj.fat_target = fat
        db_obj.carbs_target = carbs
        
        db.commit()
        db.refresh(db_obj)
        
        return db_obj

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error en update_profile_macros: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar los macros del perfil"
        )