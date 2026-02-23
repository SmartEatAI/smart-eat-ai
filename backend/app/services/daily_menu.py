from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.daily_menu import (
    get_daily_menu_by_id,
    create_daily_menu
)
from app.core.validation import ValidationService
from app.schemas.daily_menu import DailyMenuBase

class DailyMenuService:
    """Servicio para manejar operaciones relacionadas con menús diarios."""

    @staticmethod
    def get_daily_menu_by_id(db: Session, daily_menu_id: int):
        """Obtiene un menú diario por su ID."""
        try:
            daily_menu = get_daily_menu_by_id(db, daily_menu_id)
            ValidationService.validate_daily_menu_exists(daily_menu)
            return daily_menu
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error getting daily menu: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error retrieving daily menu"
            )

    @staticmethod
    def create_daily_menu(db: Session, obj_in: DailyMenuBase):
        """Crea un nuevo menú diario."""
        try:
            db_daily_menu = create_daily_menu(db, obj_in)
            ValidationService.validate_daily_menu_exists(db_daily_menu)
            return db_daily_menu
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error creating daily menu: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error creating daily menu"
            )