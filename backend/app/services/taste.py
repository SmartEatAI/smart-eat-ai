from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.taste import (
    existing_taste,
    get_tastes,
    get_taste_by_id,
    get_tastes_by_profile,
    create_taste_for_profile,
    add_taste_to_profile
)
from app.core.validation import ValidationService
from app.schemas.category import CategoryBase
from app.crud.profile import get_profile

class TasteService:
    """Servicio para manejar operaciones relacionadas con gustos."""

    @staticmethod
    def list_tastes(db: Session):
        try:
            return get_tastes(db)
        except SQLAlchemyError as e:
            print(f"Error listing tastes: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error listing tastes"
            )

    @staticmethod
    def get_taste(db: Session, taste_id: int):
        taste = get_taste_by_id(db, taste_id)
        ValidationService.validate_taste_exists(taste)
        return taste

    @staticmethod
    def get_profile_tastes(db: Session, profile_id: int):
        """Obtiene todos los gustos de un perfil específico."""
        try:
            # Obtener gustos del perfil
            tastes = get_tastes_by_profile(db, profile_id)
            return tastes
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error getting profile tastes: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving profile tastes"
            )

    @staticmethod
    def create_taste(db: Session, obj_in: CategoryBase, profile_id: int):
        try:
            # Validar que el perfil existe
            profile = get_profile(db, profile_id)
            ValidationService.validate_profile_exists(profile)
            
            # Validar que no existe un gusto con ese nombre
            existing = existing_taste(db, obj_in.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Taste already exists"
                )
            
            return create_taste_for_profile(db, obj_in, profile_id)
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error creating taste: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating taste"
            )

    @staticmethod
    def add_existing_taste(db: Session, taste_id: int, profile_id: int):
        try:
            # Validar que el perfil existe
            profile = get_profile(db, profile_id)
            ValidationService.validate_profile_exists(profile)
            
            # Validar que el gusto existe
            taste = get_taste_by_id(db, taste_id)
            ValidationService.validate_taste_exists(taste)
            
            return add_taste_to_profile(db, taste_id, profile_id)
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error adding taste to profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error adding taste to profile"
            )