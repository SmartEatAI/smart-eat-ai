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
                detail="Error retrieving tastes"
            )

    @staticmethod
    def get_taste(db: Session, taste_id: int):
        taste = get_taste_by_id(db, taste_id)
        ValidationService.validate_taste_exists(taste)
        return taste

    @staticmethod
    def get_profile_tastes(db: Session, profile_id: int):
        try:
            tastes = get_tastes_by_profile(db, profile_id)
            ValidationService.validate_profile_exists(tastes)
            return tastes
        
        except SQLAlchemyError as e:
            print(f"Error getting profile tastes: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving profile tastes"
            )

    @staticmethod
    def create_taste(db: Session, obj_in: CategoryBase, profile_id: int):
        try:
            # Validar que el gusto no exista antes de crearlo
            taste = existing_taste(db, obj_in.name)
            ValidationService.validate_taste_not_exists(taste)
            db_taste = create_taste_for_profile(db, obj_in, profile_id)
            ValidationService.validate_profile_exists(db_taste)
            return db_taste
        
        except HTTPException:
            raise
        
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error creating taste: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating taste"
            )

    @staticmethod
    def add_existing_taste(db: Session, taste_id: int, profile_id: int):
        try:
            taste = get_taste_by_id(db, taste_id)
            ValidationService.validate_taste_exists(taste)
            tastes = add_taste_to_profile(db, taste_id, profile_id)
            ValidationService.validate_profile_exists(tastes)
            
            # Validar que el gusto no esté ya asociado al perfil
            if taste in tastes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Taste already associated with profile"
                )
            result = add_taste_to_profile(db, taste_id, profile_id)
            ValidationService.validate_taste_exists(result)
            return result
        
        except HTTPException:
            raise   
        
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error adding taste to profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error adding taste to profile"
            )