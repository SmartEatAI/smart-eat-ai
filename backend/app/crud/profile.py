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
    return db.query(Profile).filter(Profile.user_id == user_id).first()

def upsert_user_profile(db: Session, obj_in: ProfileCreate, user_id: int):
    """
    Crea o actualiza el perfil de usuario.
    Calcula macros y porcentaje de grasa, luego actualiza o crea el perfil.
    """
    profile_data = calculate_macros(obj_in)
    fat_percentage = calculate_fat_percentage(obj_in)
    profile_dict = profile_data.model_dump(exclude={"tastes", "restrictions", "eating_styles"})

    profile_dict["body_fat_percentage"] = fat_percentage

    db_profile = get_profile(db, user_id=user_id)
    
    if db_profile is None:
        try:
            # Crear perfil
            new_profile = Profile(**profile_dict, user_id=user_id)
            db.add(new_profile)
            db.commit()
            db.refresh(new_profile)
            return new_profile
        except Exception as e:
            db.rollback()
            print(f"Error in upsert_user_profile, creating profile: {e}")
            raise HTTPException(status_code=500, detail="Error while creating profile")
    else:
        try:
            # Actualizar perfil sin listas de relaciones
            for field, value in profile_dict.items():
                setattr(db_profile, field, value)
            
            # Procesar Tastes y Restrictions si están en obj_in
            if hasattr(obj_in, "tastes"):
                db_profile.tastes = process_profile_categories(db, Taste, obj_in.tastes)
            if hasattr(obj_in, "restrictions"):
                db_profile.restrictions = process_profile_categories(db, Restriction, obj_in.restrictions)
            
            # Procesar Eating Styles si están en obj_in
            if hasattr(obj_in, "eating_styles"):
                styles_input = obj_in.eating_styles
                styles_instances = []
                for style in styles_input:
                    style_name = style.value if hasattr(style, "value") else style
                    style_name = style_name.lower()
                    from app.crud.eating_style import existing_eating_style
                    db_style = existing_eating_style(db, style_name)
                    if not db_style:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Eating style '{style_name}' does not exist"
                        )
                    styles_instances.append(db_style)
                db_profile.eating_styles = styles_instances
            db.commit()
            db.refresh(db_profile)
            return db_profile
        except Exception as e:
            db.rollback()
            print(f"Error in upsert_user_profile: {e}")
            raise HTTPException(status_code=500, detail="Error while updating profile")
