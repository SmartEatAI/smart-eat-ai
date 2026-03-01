from app.crud.recipe import get_recipe_by_id
from app.models.recipe import Recipe
from sqlalchemy.orm import Session
from app.models.meal_detail import MealDetail
from app.schemas.meal_detail import MealDetailCreate
from fastapi import HTTPException

def get_meal_details_by_id(db: Session, meal_detail_id: int):
    """Obtiene un detalle de comida por su ID."""
    try:
        return db.query(MealDetail).filter(MealDetail.id == meal_detail_id).first()
    except Exception as e:
        print(f"Database error when get_meal_details_by_id: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_meal_details_by_id")


def create_meal_detail(db: Session, obj_in: MealDetailCreate):
    """Crea un nuevo detalle de comida."""
    try:
        receta = get_recipe_by_id(db, recipe_id=obj_in.recipe_id)
        if not receta:
            return None
        db_meal_detail = MealDetail(**obj_in.model_dump())
        db.add(db_meal_detail)
        db.commit()
        db.refresh(db_meal_detail)
        return db_meal_detail
    except Exception as e:
        print(f"Database error when create_meal_detail: {e}")
        raise HTTPException(status_code=500, detail="Database error when create_meal_detail")

def update_meal_detail_status(db: Session, meal_detail_id: int, status: int):
    """Actualiza el estado de un detalle de comida."""
    try:
        meal_detail = db.query(MealDetail).filter(MealDetail.id == meal_detail_id).first()
        if not meal_detail:
            return None
        meal_detail.status = status
        db.commit()
        db.refresh(meal_detail)
        return meal_detail
    except Exception as e:
        print(f"Database error when update_meal_detail_status: {e}")
        raise HTTPException(status_code=500, detail="Database error when update_meal_detail_status")

def update_meal_detail_recipe_id(db: Session, meal_detail_id: int, recipe_id: int):
    """Actualiza el ID de la receta asociada a un detalle de comida."""
    try:
        meal_detail = db.query(MealDetail).filter(MealDetail.id == meal_detail_id).first()
        print(f"Updating meal_detail_id {meal_detail_id} with new recipe_id {recipe_id}")
        if not meal_detail:
            return None
        
        recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
        if not recipe:
            print(f"Recipe with id {recipe_id} not found")
            return None
        meal_detail.recipe_id = recipe.recipe_id
        db.commit()
        db.refresh(meal_detail)
        return meal_detail
    except Exception as e:
        print(f"Database error when update_meal_detail_recipe_id: {e}")
        raise HTTPException(status_code=500, detail="Database error when update_meal_detail_recipe_id")
