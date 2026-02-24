from sqlalchemy.orm import Session
from app.models.daily_menu import DailyMenu
from app.schemas.daily_menu import DailyMenuCreate
from fastapi import HTTPException

def get_daily_menu_by_id(db: Session, daily_menu_id: int):
    """Obtiene un menú diario por su ID."""
    try:
        return db.query(DailyMenu).filter(DailyMenu.id == daily_menu_id).first()
    except Exception as e:
        print(f"Database error when get_daily_menu_by_id: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_daily_menu_by_id")

def create_daily_menu(db: Session, obj_in: DailyMenuCreate):
    """Crea un nuevo menú diario."""
    try:
        db_daily_menu = DailyMenu(**obj_in.model_dump())
        db.add(db_daily_menu)
        db.commit()
        db.refresh(db_daily_menu)
        return db_daily_menu
    except Exception as e:
        print(f"Database error when create_daily_menu: {e}")
        raise HTTPException(status_code=500, detail="Database error when create_daily_menu")