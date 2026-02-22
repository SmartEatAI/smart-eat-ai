from app.crud.recipe import get_recipe_by_id
from sqlalchemy.orm import Session
from app.models.meal_detail import MealDetail
from app.schemas.meal_detail import MealDetailBase

def get_meal_details_by_id(db: Session, meal_detail_id: int):
    """Obtiene un detalle de comida por su ID."""
    return db.query(MealDetail).filter(MealDetail.id == meal_detail_id).first()

def create_meal_detail(db: Session, obj_in: MealDetailBase):
    """Crea un nuevo detalle de comida."""
    receta = get_recipe_by_id(db, recipe_id=obj_in.recipe_id)
    if not receta:
        return None
    db_meal_detail = MealDetail(**obj_in.model_dump())
    db.add(db_meal_detail)
    db.commit()
    db.refresh(db_meal_detail)
    return db_meal_detail

def update_meal_detail_status(db: Session, meal_detail_id: int, status: int):
    """Actualiza el estado de un detalle de comida."""
    meal_detail = db.query(MealDetail).filter(MealDetail.id == meal_detail_id).first()
    if not meal_detail:
        return None
    meal_detail.status = status
    db.commit()
    db.refresh(meal_detail)
    return meal_detail

def update_meal_detail_recipe_id(db: Session, meal_detail_id: int, recipe_id: int):
    """Actualiza el ID de la receta asociada a un detalle de comida."""
    meal_detail = db.query(MealDetail).filter(MealDetail.id == meal_detail_id).first()
    if not meal_detail:
        return None
    meal_detail.recipe_id = recipe_id
    db.commit()
    db.refresh(meal_detail)
    return meal_detail