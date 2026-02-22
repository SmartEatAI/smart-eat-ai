from fastapi import HTTPException, status
from typing import Any, Optional


class ValidationService:
    """Servicio para operaciones de validación comunes."""
    
    # Validaciones relacionadas con usuarios
    @staticmethod
    def validate_user_exists(user: Any) -> None:
        """Valida que un usuario exista."""
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    
    @staticmethod
    def validate_user_not_exists(user: Optional[Any]) -> None:
        """Valida que un usuario no exista."""
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    @staticmethod
    def validate_credentials(user: Any, password_valid: bool) -> None:
        """Valida las credenciales del usuario."""
        if not user or not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    
    # Validaciones relacionadas con perfiles
    @staticmethod
    def validate_profile_exists(profile: Any) -> None:
        """Valida que un perfil exista."""
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
    
    @staticmethod
    def validate_profile_not_exists(profile: Optional[Any]) -> None:
        """Valida que un perfil no exista."""
        if profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile already exists for this user"
            )