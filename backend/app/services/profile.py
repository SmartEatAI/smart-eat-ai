from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.crud.profile import (
    exist_profile, 
    get_profile, 
    create_user_profile, 
    update_user_profile
)
from app.schemas.profile import ProfileCreate, ProfileUpdate
from app.models.profile import Profile
from app.core.database import DatabaseService
from app.core.validation import ValidationService
from fastapi import HTTPException, status


class ProfileService:
    """Servicio para manejar operaciones relacionadas con el perfil del usuario."""
    
    @staticmethod
    def profile_exists(db: Session, user_id: int) -> bool:
        """Verifica si un perfil existe para un usuario específico."""
        try:
            return exist_profile(db, user_id)
        except SQLAlchemyError as e:
            print(f"Error checking profile existence: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error checking profile"
            )
    
    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> Profile:
        """Obtiene el perfil asociado a un usuario específico."""
        try:
            profile = get_profile(db, user_id)
            # Usar ValidationService en lugar de validación manual
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
    def create_profile(db: Session, user_id: int, profile_data: ProfileCreate) -> Profile:
        """Crea un nuevo perfil para un usuario específico."""
        # Validate database connection
        DatabaseService.validate_db_session(db)
        
        try:
            existing_profile = get_profile(db, user_id) if exist_profile(db, user_id) else None
            # Usar ValidationService en lugar de validación manual
            ValidationService.validate_profile_not_exists(existing_profile)
            
            return create_user_profile(db, profile_data, user_id)
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            DatabaseService.rollback_on_error(db)
            print(f"Error creating profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating profile"
            )

    @staticmethod
    def update_profile(db: Session, user_id: int, profile_data: ProfileUpdate) -> Profile:
        """Actualiza el perfil de un usuario específico."""
        try:
            profile = get_profile(db, user_id)
            # Usar ValidationService en lugar de validación manual
            ValidationService.validate_profile_exists(profile)
            
            return update_user_profile(db, db_obj=profile, obj_in=profile_data.model_dump(exclude_unset=True))
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            DatabaseService.rollback_on_error(db)
            print(f"Error updating profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating profile"
            )