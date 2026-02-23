from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.recipe import (
    get_recipe_by_id,
    get_recipes_by_meal_type,
    get_recipes_by_diet_type
)
from app.core.validation import ValidationService

class RecipeService:
    @staticmethod
    def get_recipe(db: Session, recipe_id: int):
        recipe = get_recipe_by_id(db, recipe_id)
        ValidationService.validate_recipe_exists(recipe)
        return recipe

    @staticmethod
    def get_recipes_by_meal_type(db: Session, meal_type_id: int):
        try:
            return get_recipes_by_meal_type(db, meal_type_id)
        except SQLAlchemyError as e:
            print(f"Error getting recipes by meal type: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving recipes by meal type")

    @staticmethod
    def get_recipes_by_diet_type(db: Session, diet_type_id: int):
        try:
            return get_recipes_by_diet_type(db, diet_type_id)
        except SQLAlchemyError as e:
            print(f"Error getting recipes by diet type: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving recipes by diet type")