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
                detail="Error retrieving restrictions"
            )

    @staticmethod
    def get_restriction(db: Session, restriction_id: int):
        restriction = get_restriction_by_id(db, restriction_id)
        ValidationService.validate_restriction_exists(restriction)
        return restriction

    @staticmethod
    def get_profile_restrictions(db: Session, profile_id: int):
        try:
            restrictions = get_restrictions_by_profile(db, profile_id)
            ValidationService.validate_profile_exists(restrictions)
            return restrictions
        except SQLAlchemyError as e:
            print(f"Error getting profile restrictions: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving profile restrictions"
            )

    @staticmethod
    def create_restriction(db: Session, obj_in: CategoryBase, profile_id: int):
        try:
            restriction = existing_restriction(db, obj_in.name)
            ValidationService.validate_restriction_not_exists(restriction)
            db_restriction = create_restriction_for_profile(db, obj_in, profile_id)
            ValidationService.validate_profile_exists(db_restriction)
            return db_restriction
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error creating restriction: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating restriction"
            )

    @staticmethod
    def add_existing_restriction(db: Session, restriction_id: int, profile_id: int):
        try:
            restriction = get_restriction_by_id(db, restriction_id)
            ValidationService.validate_restriction_exists(restriction)
            restrictions = get_restrictions_by_profile(db, profile_id)
            ValidationService.validate_profile_exists(restrictions)
            if restriction in restrictions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Restriction already associated with profile"
                )
            result = add_restriction_to_profile(db, restriction_id, profile_id)
            ValidationService.validate_restriction_exists(result)
            return result
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error adding restriction to profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error adding restriction to profile"
            )