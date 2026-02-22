from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.plan import (
    get_plan_by_current_user,
    deactivate_current_plan,
    create_plan
)
from app.crud.profile import exist_profile
from app.core.validation import ValidationService
from app.schemas.plan import PlanBase

class PlanService:
    """Servicio para manejar operaciones relacionadas con planes."""

    @staticmethod
    def get_current_plan(db: Session, user_id: int):
        try:
            plan = get_plan_by_current_user(db, user_id)
            ValidationService.validate_profile_exists(exist_profile(db, user_id))
            if not plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Active plan not found for current user"
                )
            return plan
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error getting current plan: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error retrieving plan"
            )

    @staticmethod
    def create_plan(db: Session, obj_in: PlanBase, user_id: int):
        try:
            ValidationService.validate_profile_exists(exist_profile(db, user_id))
            deactivate_current_plan(db, user_id)
            new_plan = create_plan(db, obj_in, user_id)
            return new_plan
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error creating plan: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error creating plan"
            )