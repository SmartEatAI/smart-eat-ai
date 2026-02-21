from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.plan import Plan
from app.schemas.plan import PlanBase
from app.crud.profile import exist_profile, update_profile_macros
from app.utils.calculations import calculate_macros


def get_plan_by_current_user(db: Session, user_id: int):
  """Obtiene el plan del usuario actual."""
  try:
    return db.query(Plan).filter(Plan.user_id == user_id, Plan.active == True).first()
  except Exception as e:
    print(f"Error al obtener plan por usuario: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar el plan en la base de datos"
    )

def deactivate_current_plan(db: Session, user_id: int):
  """Desactiva el plan activo del usuario actual."""
  try:
    db_plan = db.query(Plan).filter(Plan.user_id == user_id, Plan.active == True).first()
    if db_plan:
      db_plan.active = False
      db.commit()
  except Exception as e:
    db.rollback()
    print(f"Error al desactivar plan existente: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al desactivar el plan existente en la base de datos"
    )
  
def create_plan(db: Session, obj_in: PlanBase, user_id: int):
  """Crea un nuevo plan para el usuario actual."""

  profile = exist_profile(db, user_id=user_id)
  if not profile:
    raise ValueError(f"No existe un profile asociado al user_id: {user_id}")
  
  # Desactiva el plan activo actual antes de crear uno nuevo
  deactivate_current_plan(db, user_id)

  new_plan = Plan(**obj_in.model_dump(), user_id=user_id)
  try:
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan
  except Exception as e:
    db.rollback()
    print(f"Error al crear plan: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al crear el plan en la base de datos"
    )
