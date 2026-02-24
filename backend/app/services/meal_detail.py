from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.meal_detail import (
    get_meal_details_by_id,
    create_meal_detail,
    update_meal_detail_status,
    update_meal_detail_recipe_id
)
from app.crud.recipe import get_recipe_by_id
from app.core.validation import ValidationService
from app.schemas.meal_detail import MealDetailCreate, MealDetailResponse

class MealDetailService:
    """Servicio para manejar operaciones relacionadas con detalles de comida."""

    @staticmethod
    def get_meal_detail_by_id(db: Session, meal_detail_id: int):
        try:
            meal_detail = get_meal_details_by_id(db, meal_detail_id)
            ValidationService.validate_meal_detail_exists(meal_detail)
            return meal_detail
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error getting meal detail: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error retrieving meal detail"
            )

    @staticmethod
    def create_meal_detail(db: Session, obj_in: MealDetailCreate):
        try:
            receta = get_recipe_by_id(db, recipe_id=obj_in.recipe_id)
            ValidationService.validate_recipe_exists(receta)
            db_meal_detail = create_meal_detail(db, obj_in)
            ValidationService.validate_meal_detail_exists(db_meal_detail)
            response = MealDetailResponse.from_orm(db_meal_detail)
            response.recipe = receta
            return response
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error creating meal detail: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error creating meal detail"
            )

    @staticmethod
    def update_meal_detail_status(db: Session, meal_detail_id: int, status: int):
        try:
            meal_detail = update_meal_detail_status(db, meal_detail_id, status)
            ValidationService.validate_meal_detail_exists(meal_detail)
            return meal_detail
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error updating meal detail status: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error updating meal detail status"
            )

    @staticmethod
    def update_meal_detail_recipe_id(db: Session, meal_detail_id: int, recipe_id: int):
        try:
            meal_detail = update_meal_detail_recipe_id(db, meal_detail_id, recipe_id)
            ValidationService.validate_meal_detail_exists(meal_detail)
            return meal_detail
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error updating meal detail recipe: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error updating meal detail recipe"
            )