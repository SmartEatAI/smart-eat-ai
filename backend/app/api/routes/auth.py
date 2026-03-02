from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth import AuthService
from app.api.deps import get_current_user
from app.models.user import User
from app.core.security import verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    result = AuthService.register_user(db, user_data)
    return result


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token."""
    result = AuthService.authenticate_user(db, user_data)
    return result


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@router.get("/", response_model=bool)
def verify_token_endpoint(token: str):
    """Endpoint to verify if a token is valid."""
    try:
        payload = verify_token(token)
        return True if payload else False
    except Exception:
        return False
