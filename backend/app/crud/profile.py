from http.client import HTTPException
from app.utils.calculations import calculate_macros
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
    profile = calculate_macros(obj_in)

    db_profile = Profile(**profile.model_dump(), user_id=user_id)
    try:
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile
    except Exception as e:
        db.rollback()
        print(f"Error al crear el perfil: {e}")
        raise e

def update_user_profile(db: Session, *, db_obj: Profile, obj_in: ProfileUpdate) -> Profile:
    """
    Actualiza el perfil. 
    obj_in debe ser el diccionario de datos (puedes usar model_dump(exclude_unset=True)).
    """
    update_profile = calculate_macros(obj_in)

    db_profile = update_profile.model_dump()

    try:
        # Procesar Tastes
        if "tastes" in db_profile:
            db_obj.tastes = process_profile_categories(db, Taste, db_profile.pop("tastes"))

        # Procesar Restrictions
        if "restrictions" in db_profile:
            db_obj.restrictions = process_profile_categories(db, Restriction, db_profile.pop("restrictions"))

        # Procesar Eating Styles
        if "eating_styles" in db_profile:
            styles_input = db_profile.pop("eating_styles")
    
            styles_instances = []
    
            for style in styles_input:
                style_name = style.value if hasattr(style, "value") else style
                style_name = style_name.lower()

                # Solucion temporal para evitar error de importación circular entre profile.py y eating_style.py
                from app.crud.eating_style import existing_eating_style
                db_style = existing_eating_style(db, style_name)
    
                if not db_style:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Eating style '{style_name}' no existe"
                    )

                styles_instances.append(db_style)

            db_obj.eating_styles = styles_instances

        # Actualizar resto de campos del perfil
        for field, value in db_profile.items():
            setattr(db_obj, field, value)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj

    except Exception as e:
        db.rollback()
        print(f"Error en update_user_profile: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el perfil")