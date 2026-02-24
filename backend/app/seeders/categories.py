from sqlalchemy.orm import Session
from app.schemas.category import CategoryBase
from app.crud.diet_type import create_diet_type, existing_diet_type
from app.crud.meal_type import create_meal_type, existing_meal_type


# Diet Types
def seed_diet_types(db: Session):
    diet_types = [
        "high_protein",
        "low_carb",
        "vegan",
        "vegetarian",
        "low_calorie",
        "high_fiber",
        "high_carb",
    ]

    for name in diet_types:
        category_schema = CategoryBase(name=name)

        exists = existing_diet_type(db, category_schema.name)

        if not exists:
            create_diet_type(db, category_schema)

    db.commit()
    print("🌱 Diet types seeded")


# Meal Types
def seed_meal_types(db: Session):
    meal_types = [
        "breakfast",
        "lunch",
        "dinner",
        "snack",
        #"dessert",
        #"brunch",
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
    seed_diet_types(db)
    print("🌱 Categories seeding completed")
