from sqlalchemy.orm import Session
from app.models.plan import Plan
from app.schemas.plan import PlanBase

def get_plan_by_current_user(db: Session, user_id: int):
    """Obtiene el plan activo del usuario actual."""
    return db.query(Plan).filter(Plan.user_id == user_id, Plan.active == True).first()

def deactivate_current_plan(db: Session, user_id: int):
    """Desactiva el plan activo del usuario actual."""
    db_plan = db.query(Plan).filter(Plan.user_id == user_id, Plan.active == True).first()
    if db_plan:
        db_plan.active = False
        db.commit()

def create_plan(db: Session, obj_in: PlanBase, user_id: int):
    """Crea un nuevo plan para el usuario actual, desactivando el plan anterior si existe."""
    new_plan = Plan(**obj_in.model_dump(), user_id=user_id)
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan