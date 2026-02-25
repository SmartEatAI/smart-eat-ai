import os
import json
from sqlalchemy.orm import Session
from app.crud.recipe import create_recipe
from app.schemas.recipe import RecipeCreate


def seed_recipes(db: Session):
    # Ruta absoluta basada en la ubicación de este archivo
    current_dir = os.path.dirname(os.path.abspath(__file__))
    recipes_path = os.path.join(current_dir, "..", "data", "recipes.json")

    with open(recipes_path, encoding="utf-8") as f:
        recipes_data = json.load(f)

    for recipe_data in recipes_data:
        create_recipe(db, recipe_data)

    db.commit()
    print("🌱 Recipes seeded successfully")