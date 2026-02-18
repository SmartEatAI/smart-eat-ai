from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> dict:
        """Register a new user."""
        # Check if user already exists
        existing_user = db.query(Usuario).filter(Usuario.email == user_data.email.lower()).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        db_user = Usuario(
            name=user_data.name,
            email=user_data.email.lower(),
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
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
        user = db.query(Usuario).filter(Usuario.email == user_data.email.lower()).first()
        
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
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Usuario:
        """Get user by email."""
        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
