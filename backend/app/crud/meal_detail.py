from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.meal_detail import MealDetail
from app.schemas.meal_detail import MealDetailBase

def get_meal_details_by_id(db: Session, meal_detail_id: int):
  """Obtiene un detalle de comida por su ID."""
  try:
    return db.query(MealDetail).filter(MealDetail.id == meal_detail_id).first()
  except Exception as e:
    print(f"Error al obtener detalle de comida por ID: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar los detalles de comida en la base de datos"
    )

def get_meal_details_by_daily_menu_id(db: Session, daily_menu_id: int):
  """Obtiene los detalles de comida por su ID de menú diario."""
  try:
    return db.query(MealDetail).filter(MealDetail.daily_menu_id == daily_menu_id).all()
  except Exception as e:
    print(f"Error al obtener detalles de comida por ID de menú diario: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar los detalles de comida en la base de datos"
    )

def create_meal_detail(db: Session, obj_in: MealDetailBase):
  """Crea un nuevo detalle de comida."""
  db_meal_detail = MealDetail(**obj_in.model_dump())
  try:
    db.add(db_meal_detail)
    db.commit()
    db.refresh(db_meal_detail)
    return db_meal_detail
  except Exception as e:
    print(f"Error al crear detalle de comida: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al crear el detalle de comida en la base de datos"
    )

def update_meal_detail_status(db: Session, meal_detail_id: int, status: int):
  """Actualiza el estado de un detalle de comida."""
  try:
    meal_detail = db.query(MealDetail).filter(MealDetail.id == meal_detail_id).first()
    if not meal_detail:
      raise HTTPException(status_code=404, detail="Detalle de comida no encontrado")

    meal_detail.status = status
    db.commit()
    db.refresh(meal_detail)
    return meal_detail
  except Exception as e:
    print(f"Error al actualizar estado del detalle de comida: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al actualizar el detalle de comida en la base de datos"
    )

def update_meal_detail_recipe_id(db: Session, meal_detail_id: int, recipe_id: int):
  """Actualiza la receta de un detalle de comida."""
  try:
    meal_detail = db.query(MealDetail).filter(MealDetail.id == meal_detail_id).first()
    if not meal_detail:
      raise HTTPException(status_code=404, detail="Detalle de comida no encontrado")

    meal_detail.recipe_id = recipe_id
    db.commit()
    db.refresh(meal_detail)
    return meal_detail
  except Exception as e:
    print(f"Error al actualizar receta del detalle de comida: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al actualizar el detalle de comida en la base de datos"
    )