from sqlalchemy.orm import Session

from app.models import DietType, EatingStyle, MealType
from app.schemas.category import CategoryBase
from app.crud.diet_type import create_diet_type, existing_diet_type
from app.crud.eating_style import create_eating_style, existing_eating_style
from app.crud.meal_type import create_meal_type, existing_meal_type

categories = [
        "high_protein",
        "low_carb",
        "vegan",
        "vegetarian",
        "low_calorie",
        "high_fiber",
        "high_carb",
    ]

# Diet Types
def seed_diet_types(db: Session):

    for name in categories:
        category_schema = CategoryBase(name=name)

        exists = existing_diet_type(db, category_schema.name)

        if not exists:
            create_diet_type(db, category_schema)

    db.commit()
    print("🌱 Diet types seeded")


# Eating Styles
def seed_eating_styles(db: Session):

    for name in categories:
        category_schema = CategoryBase(name=name)

        exists = existing_eating_style(db, category_schema.name)

        if not exists:
            create_eating_style(db, category_schema)

    db.commit()
    print("🌱 Eating styles seeded")


# Meal Types
def seed_meal_types(db: Session):
    meal_types = [
        "breakfast",
        "lunch",
        "dinner",
        "snack",
        "dessert",
        "brunch",
    ]

    for name in meal_types:
        category_schema = CategoryBase(name=name)

        exists = existing_meal_type(db, category_schema.name)

        if not exists:
            create_meal_type(db, category_schema)

    db.commit()
    print("🌱 Meal types seeded")


# Seed Categorias
def seed_categories(db: Session):
    seed_meal_types(db)
    seed_eating_styles(db)
    seed_diet_types(db)
    print("🌱 Categories seeding completed")
