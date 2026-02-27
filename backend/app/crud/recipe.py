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
  
def create_recipe(db: Session, recipe_data):
    """Crea una nueva receta en la base de datos y asigna correctamente las relaciones many-to-many."""
    # Si recipe_data es un modelo Pydantic, conviértelo a dict
    if hasattr(recipe_data, 'dict'):
        recipe_dict = recipe_data.dict()
    else:
        recipe_dict = dict(recipe_data)

    meal_types = recipe_dict.pop("meal_types", [])
    diet_types = recipe_dict.pop("diet_types", [])
    
    db_recipe = Recipe(**recipe_dict)
    db.add(db_recipe)

    # Asigna relaciones many-to-many antes del commit
    if meal_types:
        db_recipe.meal_types = process_categories(db, MealType, meal_types)
    if diet_types:
        db_recipe.diet_types = process_categories(db, DietType, diet_types)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe