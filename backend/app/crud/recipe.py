from app.models.meal_type import MealType
from app.models.diet_type import DietType
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.recipe import Recipe

def get_recipe_by_id(db: Session, recipe_id: int):
  """Obtiene una receta por su ID."""
  try:
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()
  except Exception as e:
    print(f"Error al obtener receta por ID: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar las recetas en la base de datos"
    )

def get_recipes_by_meal_type(db: Session, meal_type_id: int):
  """Obtiene las recetas por su tipo de comida."""
  try:
    return db.query(Recipe).filter(Recipe.meal_types.any(MealType.id == meal_type_id)).all()
  except Exception as e:
    print(f"Error al obtener receta por tipo de comida: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar las recetas en la base de datos"
    )

def get_recipes_by_diet_type(db: Session, diet_type_id: int):
  """Obtiene las recetas por su tipo de dieta."""
  print(f"Consultando recetas para diet_type_id: {diet_type_id}")
  try:
    recipes = db.query(Recipe).filter(Recipe.diet_types).all()
    print(f"Recetas encontradas: {recipes}")
    return recipes
  except Exception as e:
    print(f"Error al obtener receta por tipo de dieta: {str(e)}")

    raise HTTPException(
      status_code=500, 
      detail="Error interno al consultar las recetas en la base de datos"
    )