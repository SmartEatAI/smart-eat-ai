from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.meal_type import (
    get_meal_types,
    get_meal_type_by_id
)
from app.core.validation import ValidationService

class MealTypeService:
    """Servicio para manejar operaciones relacionadas con tipos de comida."""

    @staticmethod
    def list_meal_types(db: Session):
        try:
            return get_meal_types(db)
        except SQLAlchemyError as e:
            print(f"Error listing meal types: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving meal types"
            )

    @staticmethod
    def get_meal_type(db: Session, meal_type_id: int):
        meal_type = get_meal_type_by_id(db, meal_type_id)
        ValidationService.validate_meal_type_exists(meal_type)
        return meal_type