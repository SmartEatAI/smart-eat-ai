from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Recupera un usuario por su correo electrónico."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: UserCreate) -> User:
    """Crea un nuevo usuario."""
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