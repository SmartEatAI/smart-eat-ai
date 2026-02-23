from sqlalchemy.orm import Session
from app.crud.recipe import create_recipe


def seed_recipes(db: Session):

    recipes_data = [
        {
            "name": "High Protein Omelette",
            "calories": 350,
            "protein": 30,
            "carbs": 5,
            "fat": 22,
            "meal_types": ["breakfast"],
            "diet_types": ["high_protein", "low_carb"],
        },
        {
            "name": "Vegan Buddha Bowl",
            "calories": 500,
            "protein": 18,
            "carbs": 65,
            "fat": 18,
            "meal_types": ["lunch", "dinner"],
            "diet_types": ["vegan", "high_fiber"],
        },
        {
            "name": "Chicken & Rice Muscle Bowl",
            "calories": 700,
            "protein": 55,
            "carbs": 80,
            "fat": 15,
            "meal_types": ["lunch", "dinner"],
            "diet_types": ["high_protein", "high_carb"],
        },
        {
            "name": "Low Carb Salmon Salad",
            "calories": 450,
            "protein": 40,
            "carbs": 10,
            "fat": 28,
            "meal_types": ["dinner"],
            "diet_types": ["low_carb"],
        },
        {
            "name": "Vegetarian Quinoa Salad",
            "calories": 400,
            "protein": 15,
            "carbs": 50,
            "fat": 12,
            "meal_types": ["lunch"],
            "diet_types": ["vegetarian", "high_fiber"],
        },
    ]

    for recipe_data in recipes_data:
        create_recipe(db, recipe_data)

    db.commit()
    print("🌱 Recipes seeded successfully")
