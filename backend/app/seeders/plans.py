from sqlalchemy.orm import Session
from app.services.plan import PlanService
from app.models import User, Recipe


def seed_plans(db: Session):
    users = db.query(User).filter(User.id.in_([1, 2, 3])).all()

    if not users:
        print("No users found for plan seeding")
        return

    # IDs de recetas a usar
    recipe_ids = [38, 39, 40]

    for user in users:
        daily_menus = []
        for i, recipe_id in enumerate(recipe_ids, start=1):
            recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
            # Obtener el primer meal_type válido asociado a la receta
            meal_type = None
            if recipe and recipe.meal_types:
                # recipe.meal_types es una lista de objetos MealType
                meal_type = recipe.meal_types[0].name
            else:
                meal_type = "breakfast"  # fallback seguro
            daily_menus.append({
                "day_of_week": i,
                "meal_details": [
                    {
                        "recipe_id": recipe_id,
                        "schedule": 1,
                        "status": 0,
                        "meal_type": meal_type
                    }
                ]
            })

        plan_schema = {
            "daily_menus": daily_menus,
            "active": True,
        }

        try:
            PlanService.create_plan(
                db=db,
                obj_in=plan_schema,
                user_id=user.id,
            )
            print(f"Plan created for user {user.id}")
        except Exception as e:
            print(f"Error creating plan for user {user.id}: {e}")

    print("🌱 Plans seeding completed")
