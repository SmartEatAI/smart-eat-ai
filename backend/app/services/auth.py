from sqlalchemy.orm import Session
from app.models.user import User
from app.models.profile import Profile
from app.schemas.user import UserCreate, UserLogin
from app.core.security import verify_password, create_access_token
from fastapi import HTTPException, status

from app.crud.user import create_user, get_user_by_email


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> dict:
        """Register a new user."""
        if db is None:
            print("ERROR: La sesión de DB es None")
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

        db_user = create_user(db, user_data)

        # Generate JWT token for automatic login
        access_token = create_access_token({"sub": db_user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": db_user
        }
    
    @staticmethod
    def authenticate_user(db: Session, user_data: UserLogin) -> dict:
        """Authenticate user and return access token."""
        user = get_user_by_email(db, user_data.email.lower())
        
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Generate JWT token
        access_token = create_access_token({"sub": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
