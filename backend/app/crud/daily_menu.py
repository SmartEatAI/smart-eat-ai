from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.meal_detail import MealDetail
from app.schemas.meal_detail import MealDetailBase

def get_daily_menu_by_id(db: Session, daily_menu_id: int):
  """Obtiene un menú diario por su ID."""
  try:
    return db.query(MealDetail).filter(MealDetail.daily_menu_id == daily_menu_id).all()
  except Exception as e:
    print(f"Error al obtener menú diario por ID: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar el menú diario en la base de datos"
    )

def get_daily_menu_by_plan_id(db: Session, plan_id: int):
  """Obtiene un menú diario por su ID de plan."""
  try:
    return db.query(MealDetail).filter(MealDetail.plan_id == plan_id).all()
  except Exception as e:
    print(f"Error al obtener menú diario por ID de plan: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar el menú diario en la base de datos"
    )

def create_daily_menu(db: Session, obj_in: MealDetailBase):
  """Crea un nuevo menú diario."""
  db_meal_detail = MealDetail(**obj_in.model_dump())
  try:
    db.add(db_meal_detail)
    db.commit()
    db.refresh(db_meal_detail)
    return db_meal_detail
  except Exception as e:
    print(f"Error al crear menú diario: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al crear el menú diario en la base de datos"
    )