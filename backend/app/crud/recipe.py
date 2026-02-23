from app.models.meal_type import MealType
from app.models.diet_type import DietType
from app.schemas.recipe import RecipeCreate
from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from fastapi import HTTPException
from app.crud.category import process_categories

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
  fields_to_remove = ["diet_types", "meal_types"]

  recipe_dict = recipe_data
  
  for field in fields_to_remove:
    recipe_dict.pop(field, None)

  db_recipe = Recipe(**recipe_dict)
  db.add(db_recipe)

  if hasattr(recipe_data, "meal_types"):
    db_recipe.meal_types = process_categories(db, MealType, recipe_data.meal_types)

  if hasattr(recipe_data, "restrictions"):
    db_recipe.diet_types = process_categories(db, DietType, recipe_data.diet_types)
            
  db.commit()
  db.refresh(db_recipe)
  return db_recipe