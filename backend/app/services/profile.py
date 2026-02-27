from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.profile import (
    exist_profile,
    get_profile,
    create_profile,
    update_profile
)
from app.models.taste import Taste
from app.models.restriction import Restriction
from app.crud.category import process_categories
from app.schemas.profile import ProfileCreate
from app.utils.calculations import calculate_macros, calculate_fat_percentage
from app.core.validation import ValidationService

class ProfileService:
    """Servicio para manejar operaciones relacionadas con el perfil del usuario."""

    @staticmethod
    def profile_exists(db: Session, user_id: int) -> bool:
        try:
            return exist_profile(db, user_id)
        except SQLAlchemyError as e:
            print(f"Error checking profile existence: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error checking profile"
            )

    @staticmethod
    def get_user_profile(db: Session, user_id: int):
        try:
            profile = get_profile(db, user_id)
            ValidationService.validate_profile_exists(profile)
            return profile
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error getting profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving profile"
            )

    @staticmethod
    def upsert_user_profile(db: Session, obj_in: ProfileCreate, user_id: int):
        profile_data = calculate_macros(obj_in)
        fat_percentage = calculate_fat_percentage(obj_in)
        profile_dict = profile_data.model_dump(exclude={'tastes', 'restrictions', 'diet_types'})
        profile_dict["body_fat_percentage"] = fat_percentage

        db_profile = get_profile(db, user_id)
        try:
            if db_profile is None:
                db_profile = create_profile(db, profile_dict, user_id)
            else:
                db_profile = update_profile(db, db_profile, profile_dict)

            # Asignar relaciones en ambos casos
            if hasattr(obj_in, "tastes"):
                db_profile.tastes = process_categories(db, Taste, obj_in.tastes)
            if hasattr(obj_in, "restrictions"):
                db_profile.restrictions = process_categories(db, Restriction, obj_in.restrictions)
            if hasattr(obj_in, "diet_types"):
                styles_input = obj_in.diet_types
                styles_instances = []
                for style in styles_input:
                    style_name = style.value if hasattr(style, "value") else style
                    style_name = style_name.lower()
                    from app.crud.diet_type import existing_diet_type
                    db_style = existing_diet_type(db, style_name)
                    if not db_style:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Diet type '{style_name}' does not exist"
                        )
                    styles_instances.append(db_style)
                db_profile.diet_types = styles_instances

            db.commit()
            db.refresh(db_profile)
            return db_profile
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            print(f"Error in upsert_user_profile: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Error while updating profile")