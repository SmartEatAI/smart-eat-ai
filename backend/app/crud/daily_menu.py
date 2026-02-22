from sqlalchemy.orm import Session
from app.models.daily_menu import DailyMenu
from app.schemas.daily_menu import DailyMenuBase

def get_daily_menu_by_id(db: Session, daily_menu_id: int):
    """Obtiene un menú diario por su ID."""
    return db.query(DailyMenu).filter(DailyMenu.id == daily_menu_id).first()

def create_daily_menu(db: Session, obj_in: DailyMenuBase):
    """Crea un nuevo menú diario."""
    db_daily_menu = DailyMenu(**obj_in.model_dump())
    db.add(db_daily_menu)
    db.commit()
    db.refresh(db_daily_menu)
    return db_daily_menu