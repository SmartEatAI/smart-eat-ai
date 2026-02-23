from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from fastapi import HTTPException


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Recupera un usuario por su correo electrónico."""
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        print(f"Database error when get_user_by_email: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_user_by_email")


def create_user(db: Session, user_data: UserCreate) -> User:
    """Crea un nuevo usuario."""
    try:
        email_limpio = user_data.email.lower().strip()

        hashed_password = hash_password(user_data.password)
        db_user = User(
            name=user_data.name,
            email=email_limpio,
            hashed_password=hashed_password
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Database error when create_user: {e}")
        raise HTTPException(status_code=500, detail="Database error when create_user")