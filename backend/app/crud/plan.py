from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.plan import Plan
from app.schemas.plan import PlanBase

def get_plan_by_current_user(db: Session, user_id: int):
  """Obtiene el plan del usuario actual."""
  try:
    return db.query(Plan).filter(Plan.user_id == user_id).first()
  except Exception as e:
    print(f"Error al obtener plan por usuario: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar el plan en la base de datos"
    )

def create_plan(db: Session, obj_in: PlanBase, user_id: int):
  """Crea un nuevo plan para el usuario actual."""
  db_plan = db.query(Plan).filter(Plan.user_id == user_id).first()
  if db_plan:
    # Si el usuario ya tiene un plan, lo desactivamos con active = False
    db_plan.active = False
    db.commit()

  new_plan = Plan(**obj_in.model_dump(), user_id=user_id)
  try:
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan
  except Exception as e:
    print(f"Error al crear plan: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al crear el plan en la base de datos"
    )

def update_plan_status(db: Session, plan_id: int, active: bool):
  """Actualiza el estado de un plan."""
  try:
    db_plan = db.query(Plan).filter(Plan.active == True).first()
    if db_plan:
      db_plan.active = False
      db.commit()

    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
      raise HTTPException(status_code=404, detail="Plan no encontrado")

    plan.active = active
    db.commit()
    db.refresh(plan)
    return plan
  except Exception as e:
    print(f"Error al actualizar estado del plan: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al actualizar el estado del plan en la base de datos"
    )