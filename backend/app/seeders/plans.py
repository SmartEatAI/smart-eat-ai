from sqlalchemy.orm import Session
from app.services.plan import PlanService
from app.models import User, Recipe

def seed_plans(db: Session):
    users = db.query(User).filter(User.id.in_([1, 2, 3])).all()

    if not users:
        print("No users found for plan seeding")
        return

    # Obtén todos los IDs de recetas disponibles
    recipe_ids = [r.id for r in db.query(Recipe).all()]
    if len(recipe_ids) < 28:
        print("No hay suficientes recetas para 4 por día durante 7 días")
        return

    for user in users:
        daily_menus = []
        for day in range(1, 8):  # 7 días
            meal_details = []
            # Selecciona 4 recetas distintas para cada día
            day_recipe_ids = recipe_ids[(day-1)*4 : day*4]
            for idx, recipe_id in enumerate(day_recipe_ids):
                recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
                meal_type = recipe.meal_types[0].name if recipe and recipe.meal_types else "breakfast"
                meal_details.append({
                    "recipe_id": recipe_id,
                    "schedule": idx+1,
                    "status": 0,
                    "meal_type": meal_type
                })
            daily_menus.append({
                "day_of_week": day,
                "meal_details": meal_details
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