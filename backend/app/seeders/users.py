from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.auth import AuthService
from app.schemas.user import UserCreate
from app.crud.user import get_user_by_email


def seed_users(db: Session):
    users_data = [
        {
            "name": "Ruyi",
            "email": "ruyi@example.com",
            "password": "Ruyi1234",
        },
        {
            "name": "Elias",
            "email": "elias@example.com",
            "password": "Elias1234",
        },
        {
            "name": "Cristina",
            "email": "cristina@example.com",
            "password": "Cris1234",
        },
    ]


    for user_data in users_data:
        existing_user = get_user_by_email(db, user_data["email"])

        if existing_user:
            print(f"Use already exists: {user_data['email']}")
            continue
        
        try:
            user_schema = UserCreate(**user_data)
            AuthService.register_user(db, user_schema)
            print(f"User created: {user_data['email']}")
        except HTTPException as e:
            print(f"Error creating user {user_data['email']}: {e.detail}")

    print("🌱 User seeding finished.")
