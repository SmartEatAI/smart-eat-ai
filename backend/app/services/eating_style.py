from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.eating_style import (
    existing_eating_style,
    get_eating_styles,
    get_eating_style_by_id,
    get_eating_styles_by_profile,
    create_eating_style_for_profile,
    add_eating_style_to_profile
)
from app.core.validation import ValidationService
from app.schemas.category import CategoryBase

class EatingStyleService:
    """Servicio para manejar operaciones relacionadas con estilos de alimentación."""

    @staticmethod
    def list_eating_styles(db: Session):
        try:
            return get_eating_styles(db)
        except SQLAlchemyError as e:
            print(f"Error listing eating styles: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving eating styles"
            )

    @staticmethod
    def get_eating_style(db: Session, eating_style_id: int):
        eating_style = get_eating_style_by_id(db, eating_style_id)
        ValidationService.validate_eating_style_exists(eating_style)
        return eating_style

    @staticmethod
    def get_profile_eating_styles(db: Session, profile_id: int):
        try:
            styles = get_eating_styles_by_profile(db, profile_id)
            return styles
        except SQLAlchemyError as e:
            print(f"Error getting profile eating styles: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving profile eating styles"
            )

    @staticmethod
    def create_eating_style(db: Session, obj_in: CategoryBase, profile_id: int):
        try:
            eating_style = existing_eating_style(db, obj_in.name)
            ValidationService.validate_eating_style_not_exists(eating_style)
            db_eating_style = create_eating_style_for_profile(db, obj_in, profile_id)
            ValidationService.validate_profile_exists(db_eating_style)
            return db_eating_style
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
    def add_existing_eating_style(db: Session, eating_style_id: int, profile_id: int):
        try:
            eating_style = get_eating_style_by_id(db, eating_style_id)
            ValidationService.validate_eating_style_exists(eating_style)
            styles = get_eating_styles_by_profile(db, profile_id)
            ValidationService.validate_profile_exists(styles)
            if eating_style in styles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Eating style already associated with profile"
                )
            result = add_eating_style_to_profile(db, eating_style_id, profile_id)
            ValidationService.validate_eating_style_exists(result)
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