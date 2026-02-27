from sqlalchemy.orm import Session
from app.services.plan import PlanService
from app.models import User


def seed_plans(db: Session):
    users = db.query(User).filter(User.id.in_([1, 2, 3])).all()

    if not users:
        print("No users found for plan seeding")
        return

    for user in users:

        plan_schema = {
            "daily_menus": [
                {
                  "day_of_week": 1,
                  "meal_details": [
                      {
                        "recipe_id": 38,
                        "schedule": 1,
                        "status": 0,
                        "meal_type": "breakfast"
                      },
                      {
                        "recipe_id": 38,
                        "schedule": 1,
                        "status": 0,
                        "meal_type": "breakfast"
                      },{
                        "recipe_id": 38,
                        "schedule": 1,
                        "status": 0,
                        "meal_type": "breakfast"
                      }
                  ]
                },
                {
                  "day_of_week": 2,
                  "meal_details": [
                      {
                        "recipe_id": 39,
                        "schedule": 1,
                        "status": 0,
                        "meal_type": "breakfast"
                      }
                  ]
                },
                {
                  "day_of_week": 3,
                  "meal_details": [
                      {
                        "recipe_id": 40,
                        "schedule": 1,
                        "status": 0,
                        "meal_type": "breakfast"
                      }
                  ]
                },
            ],
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
