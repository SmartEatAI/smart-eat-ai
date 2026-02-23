import datetime
from sqlalchemy.orm import Session
from app.services.profile import ProfileService
from app.schemas.profile import ProfileCreate
from app.models import User


def seed_profiles(db: Session):
    users = db.query(User).filter(User.id.in_([1, 2, 3])).all()

    if not users:
        print("No users found for profile seeding")
        return

    profiles_data = {
        1: {
            "goal": "lose_weight",
            "height": 175,
            "weight": 85,
            "body_type": "stocky",
            "gender": "male",
            "meals_per_day": 3,
            "activity_level": "medium",
            "birth_date": datetime.date(1990, 5, 10),
            "eating_styles": [{"name": "high_protein"}, {"name": "low_carb"}],
            "restrictions": [{"name": "dairy_free"}],
            "tastes": [{"name": "sweet"}, {"name": "savory"}]
        },
        2: {
            "goal": "maintain_weight",
            "height": 165,
            "weight": 60,
            "body_type": "normal",
            "gender": "female",
            "meals_per_day": 4,
            "activity_level": "high",
            "birth_date": datetime.date(1995, 8, 22),
            "eating_styles": [{"name": "vegetarian"}, {"name": "high_fiber"}],
            "restrictions": [{"name": "nut_free"}],
            "tastes": [{"name": "spicy"}, {"name": "bitter"}]
        },
        3: {
            "goal": "gain_weight",
            "height": 180,
            "weight": 70,
            "body_type": "lean",
            "gender": "male",
            "meals_per_day": 5,
            "activity_level": "high",
            "birth_date": datetime.date(1998, 3, 15),
            "eating_styles": [{"name": "high_carb"}, {"name": "high_protein"}],
            "restrictions": [{"name": "gluten_free"}],
            "tastes": [{"name": "spicy"}, {"name": "savory"}]
        },
    }

    for user in users:
        profile_payload = profiles_data.get(user.id)

        if not profile_payload:
            continue

        profile_schema = ProfileCreate(**profile_payload)

        ProfileService.upsert_user_profile(
            db=db,
            obj_in=profile_schema,
            user_id=user.id,
        )

        print(f"Profile seeded for user {user.id}")

    print("🌱 Profiles seeding completed")
