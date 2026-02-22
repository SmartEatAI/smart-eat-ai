from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.daily_menu import DailyMenu
from app.schemas.daily_menu import DailyMenuBase

def get_daily_menu_by_id(db: Session, daily_menu_id: int):
  """Obtiene un menú diario por su ID."""
  try:
    return db.query(DailyMenu).filter(DailyMenu.id == daily_menu_id).first()
  except Exception as e:
    print(f"Error al obtener menú diario por ID: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar el menú diario en la base de datos"
    )

def create_daily_menu(db: Session, obj_in: DailyMenuBase):
  """Crea un nuevo menú diario."""
  db_daily_menu = DailyMenu(**obj_in.model_dump())
  try:
    db.add(db_daily_menu)
    db.commit()
    db.refresh(db_daily_menu)
    return db_daily_menu
  except Exception as e:
    print(f"Error al crear menú diario: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al crear el menú diario en la base de datos"
    )