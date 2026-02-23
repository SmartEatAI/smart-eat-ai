from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.diet_type import (
    existing_diet_type,
    get_diet_types,
    get_diet_type_by_id,
    get_diet_types_by_profile,
    create_diet_type_for_profile,
    add_diet_type_to_profile
)
from app.core.validation import ValidationService
from app.schemas.category import CategoryBase

class DietTypeService:
    """Servicio para manejar operaciones relacionadas con estilos de alimentación."""

    @staticmethod
    def list_diet_types(db: Session):
        try:
            return get_diet_types(db)
        except SQLAlchemyError as e:
            print(f"Error listing eating styles: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving eating styles"
            )

    @staticmethod
    def get_diet_type(db: Session, diet_type_id: int):
        diet_type = get_diet_type_by_id(db, diet_type_id)
        ValidationService.validate_diet_type_exists(diet_type)
        return diet_type

    @staticmethod
    def get_profile_diet_types(db: Session, profile_id: int):
        try:
            styles = get_diet_types_by_profile(db, profile_id)
            return styles
        except SQLAlchemyError as e:
            print(f"Error getting profile eating styles: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving profile eating styles"
            )

    @staticmethod
    def create_diet_type(db: Session, obj_in: CategoryBase, profile_id: int):
        try:
            diet_type = existing_diet_type(db, obj_in.name)
            ValidationService.validate_diet_type_not_exists(diet_type)
            db_diet_type = create_diet_type_for_profile(db, obj_in, profile_id)
            ValidationService.validate_profile_exists(db_diet_type)
            return db_diet_type
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error creating eating style: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating eating style"
            )

    @staticmethod
    def add_existing_diet_type(db: Session, diet_type_id: int, profile_id: int):
        try:
            diet_type = get_diet_type_by_id(db, diet_type_id)
            ValidationService.validate_diet_type_exists(diet_type)
            styles = get_diet_types_by_profile(db, profile_id)
            ValidationService.validate_profile_exists(styles)
            if diet_type in styles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Eating style already associated with profile"
                )
            result = add_diet_type_to_profile(db, diet_type_id, profile_id)
            ValidationService.validate_diet_type_exists(result)
            return result
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error adding eating style to profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error adding eating style to profile"
            )