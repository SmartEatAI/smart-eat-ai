import datetime
from sqlalchemy.orm import Session
from app.services.plan import PlanService
from app.schemas.plan import PlanBase
from app.models import User


def seed_plans(db: Session):
    users = db.query(User).filter(User.id.in_([1, 2, 3])).all()

    if not users:
        print("No users found for plan seeding")
        return

    for user in users:
        now = datetime.datetime.now()

        plan_schema = PlanBase(
            created_at=now,
            updated_at=now,
            daily_menus=[
                {
                  "day_of_week": 1,
                  "meal_details": [
                      {
                        "recipe_id": 1,
                        "schedule": 1,
                        "status": 0,
                        "meal_type": {"name": "breakfast"}
                      }
                  ]
                },
                {
                  "day_of_week": 2,
                  "meal_details": [
                      {
                        "recipe_id": 2,
                        "schedule": 1,
                        "status": 0,
                        "meal_type": {"name": "breakfast"}
                      }
                  ]
                },
                {
                  "day_of_week": 3,
                  "meal_details": [
                      {
                        "recipe_id": 3,
                        "schedule": 1,
                        "status": 0,
                        "meal_type": {"name": "breakfast"}
                      }
                  ]
                },
            ],
            active=True,
        )

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
