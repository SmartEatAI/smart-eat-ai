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
            
    # Validaciones relacionadas con gustos
    @staticmethod
    def validate_taste_exists(taste: Any) -> None:
        """Valida que un gusto exista."""
        if not taste:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Taste not found"
            )
            
    @staticmethod
    def validate_taste_not_exists(taste: Optional[Any]) -> None:
        """Valida que un gusto no exista."""
        if taste:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Taste already exists"
            )
            
    # Validaciones relacionadas con restricciones
    @staticmethod
    def validate_restriction_exists(restriction: any) -> None:
        if not restriction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restriction not found"
            )

    @staticmethod
    def validate_restriction_not_exists(restriction: any) -> None:
        if restriction:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restriction already exists"
            )
            
    # Validaciones relacionadas con detalles de comidas y recetas
    @staticmethod
    def validate_meal_detail_exists(meal_detail: any) -> None:
        if not meal_detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal detail not found"
            )

    @staticmethod
    def validate_recipe_exists(recipe: any) -> None:
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
            
    # Validaciones relacionadas con estilos de alimentación
    @staticmethod
    def validate_eating_style_exists(eating_style: any) -> None:
        if not eating_style:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Eating style not found"
            )

    @staticmethod
    def validate_eating_style_not_exists(eating_style: any) -> None:
        if eating_style:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Eating style already exists"
            )
            
    # Validaciones relacionadas con daily menu
    @staticmethod
    def validate_daily_menu_exists(daily_menu: any) -> None:
        if not daily_menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Daily menu not found"
            )
            
    # Validaciones relacionadas con tipos de dieta
    @staticmethod
    def validate_diet_type_exists(diet_type: any) -> None:
        if not diet_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diet type not found"
            )
            
    # Validaciones relacionadas con recipe
    @staticmethod
    def validate_recipe_exists(recipe: any) -> None:
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
            
    # Validaciones relacionadas con tipos de comida
    @staticmethod
    def validate_meal_type_exists(meal_type: any) -> None:
        if not meal_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal type not found"
            )