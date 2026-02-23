from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.user import UserCreate, UserLogin
from app.core.security import verify_password, create_access_token
from app.crud.user import create_user, get_user_by_email
from app.core.database import DatabaseService
from app.core.validation import ValidationService
from fastapi import HTTPException, status


class AuthService:
    """Servicio para manejar operaciones relacionadas con la autenticación de usuarios."""
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> dict:
        """Registra un nuevo usuario y devuelve un token de acceso."""
        # Validate database connection
        DatabaseService.validate_db_session(db)
        
        try:
            # Check if user already exists
            email_limpio = user_data.email.lower().strip()
            existing_user = get_user_by_email(db, email_limpio)
            
            # Validate user doesn't exist
            ValidationService.validate_user_not_exists(existing_user)
            
            # Create new user
            db_user = create_user(db, user_data)
            
            # Generate JWT token for automatic login
            access_token = create_access_token({"sub": db_user.email})
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": db_user
            }
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            DatabaseService.rollback_on_error(db)
            print(f"Error registering user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user"
            )
    
    @staticmethod
    def authenticate_user(db: Session, user_data: UserLogin) -> dict:
        """Autentica a un usuario y devuelve un token de acceso."""
        try:
            email_limpio = user_data.email.lower().strip()
            user = get_user_by_email(db, email_limpio)
            
            # Validate credentials using ValidationService
            password_valid = verify_password(user_data.password, user.hashed_password) if user else False
            ValidationService.validate_credentials(user, password_valid)
            
            # Generate JWT token
            access_token = create_access_token({"sub": user.email})
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": user
            }
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error authenticating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error during authentication"
            )