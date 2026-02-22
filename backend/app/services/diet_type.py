from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.diet_type import get_diet_types, get_diet_type_by_id
from app.core.validation import ValidationService

class DietTypeService:
    @staticmethod
    def list_diet_types(db: Session):
        try:
            return get_diet_types(db)
        except SQLAlchemyError as e:
            print(f"Error listing diet types: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving diet types")

    @staticmethod
    def get_diet_type(db: Session, diet_type_id: int):
        diet_type = get_diet_type_by_id(db, diet_type_id)
        ValidationService.validate_diet_type_exists(diet_type)
        return diet_type