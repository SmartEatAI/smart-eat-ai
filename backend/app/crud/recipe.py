from app.models.meal_type import MealType
from app.models.diet_type import DietType
from app.schemas.recipe import RecipeCreate
from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from fastapi import HTTPException

def get_recipe_by_id(db: Session, recipe_id: int):
  """Obtiene una receta por su ID."""
  try:
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()
  except Exception as e:
        print(f"Database error when get_recipe_by_id: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_recipe_by_id")

def get_recipes_by_meal_type(db: Session, meal_type_id: int):
  """Obtiene recetas asociadas a un tipo de comida específico."""
  try:
    return db.query(Recipe).filter(Recipe.meal_types.any(MealType.id == meal_type_id)).all()
  except Exception as e:
        print(f"Database error when get_recipes_by_meal_type: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_recipes_by_meal_type")

def get_recipes_by_diet_type(db: Session, diet_type_id: int):
  """Obtiene recetas asociadas a un tipo de dieta específico."""
  try:
    return db.query(Recipe).filter(Recipe.diet_types.any(DietType.id == diet_type_id)).all()
  except Exception as e:
        print(f"Database error when get_recipes_by_diet_type: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_recipes_by_diet_type")
  
def create_recipe(db: Session, recipe_data: RecipeCreate):
  """Crea una nueva receta en la base de datos."""
  new_recipe = Recipe(**recipe_data)
  db.add(new_recipe)
  db.commit()
  db.refresh(new_recipe)
  return new_recipe