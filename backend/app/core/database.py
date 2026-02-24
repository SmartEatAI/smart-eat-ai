from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class DatabaseService:
    """Servicio para operaciones y validaciones de base de datos."""
    
    @staticmethod
    def validate_db_session(db: Session) -> None:
        """Valida que la sesión de base de datos esté activa."""
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error connecting to the database"
            )
    
    @staticmethod
    def rollback_on_error(db: Session) -> None:
        """Rollback de la transacción en caso de error."""
        try:
            db.rollback()
        except Exception as e:
            print(f"Error during rollback: {e}")