from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from fastapi import HTTPException, status


def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user."""
    email_limpio = user_data.email.lower().strip()
    existing_user = db.query(User).filter(User.email == email_limpio).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
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