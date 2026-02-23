from sqlalchemy.orm import Session
from app.models.plan import Plan
from app.schemas.plan import PlanBase
from fastapi import HTTPException

def get_plan_by_current_user(db: Session, user_id: int):
    """Obtiene el plan activo del usuario actual."""
    try:
        return db.query(Plan).filter(Plan.user_id == user_id, Plan.active == True).first()
    except Exception as e:
        print(f"Database error when get_plan_by_current_user: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_plan_by_current_user")

def deactivate_current_plan(db: Session, user_id: int):
    """Desactiva el plan activo del usuario actual."""
    try:
        db_plan = db.query(Plan).filter(Plan.user_id == user_id, Plan.active == True).first()
        if db_plan:
            db_plan.active = False
            db.commit()
    except Exception as e:
        print(f"Database error when deactivate_current_plan: {e}")
        raise HTTPException(status_code=500, detail="Database error when deactivate_current_plan")

def create_plan(db: Session, obj_in: PlanBase, user_id: int):
    """Crea un nuevo plan para el usuario actual, desactivando el plan anterior si existe."""
    try:
        new_plan = Plan(**obj_in.model_dump(), user_id=user_id)
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
        return new_plan
    except Exception as e:
        print(f"Database error when create_plan: {e}")
        raise HTTPException(status_code=500, detail="Database error when create_plan")