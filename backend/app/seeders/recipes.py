import json
from sqlalchemy.orm import Session
from app.crud.recipe import create_recipe
from app.schemas.recipe import RecipeCreate


def seed_recipes(db: Session):

    with open("app/seeders/data/recipes.json", encoding="utf-8") as f:
        recipes_data = json.load(f)

    for recipe_data in recipes_data:
        create_recipe(db, recipe_data)

    db.commit()
    print("🌱 Recipes seeded successfully")
