from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.restriction import (
    existing_restriction,
    get_restrictions,
    get_restriction_by_id,
    get_restrictions_by_profile,
    create_restriction_for_profile,
    add_restriction_to_profile
)
from app.core.validation import ValidationService
from app.schemas.category import CategoryBase
from app.crud.profile import get_profile

class RestrictionService:
    """Servicio para manejar operaciones relacionadas con restricciones."""

    @staticmethod
    def list_restrictions(db: Session):
        try:
            return get_restrictions(db)
        except SQLAlchemyError as e:
            print(f"Error listing restrictions: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error listing restrictions"
            )

    @staticmethod
    def get_restriction(db: Session, restriction_id: int):
        restriction = get_restriction_by_id(db, restriction_id)
        ValidationService.validate_restriction_exists(restriction)
        return restriction

    @staticmethod
    def get_profile_restrictions(db: Session, profile_id: int):
        """Obtiene todas las restricciones de un perfil específico."""
        try:
            # Obtener restricciones del perfil
            restrictions = get_restrictions_by_profile(db, profile_id)
            return restrictions
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error getting profile restrictions: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving profile restrictions"
            )

    @staticmethod
    def create_restriction(db: Session, obj_in: CategoryBase, profile_id: int):
        try:
            # Validar que el perfil existe
            profile = get_profile(db, profile_id)
            ValidationService.validate_profile_exists(profile)
            
            # Validar que no existe restricción con ese nombre
            existing = existing_restriction(db, obj_in.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Restriction already exists"
                )
            
            return create_restriction_for_profile(db, obj_in, profile_id)
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error creating restriction: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating restriction"
            )

    @staticmethod
    def add_existing_restriction(db: Session, restriction_id: int, profile_id: int):
        try:
            # Validar que el perfil existe
            profile = get_profile(db, profile_id)
            ValidationService.validate_profile_exists(profile)
            
            # Validar que la restricción existe
            restriction = get_restriction_by_id(db, restriction_id)
            ValidationService.validate_restriction_exists(restriction)
            
            return add_restriction_to_profile(db, restriction_id, profile_id)
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error adding restriction to profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error adding restriction to profile"
            )