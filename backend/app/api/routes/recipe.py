from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.recipe import RecipeBase, RecipeResponse
from app.crud import recipe as crud
from app.models import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/recipe", tags=["Recipe"])
@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe_by_id(
    recipe_id: int, 
    db: Session = Depends(get_db)
):
    return crud.get_recipe_by_id(db, recipe_id=recipe_id)

@router.get("/list-by-meal-type/{meal_type}", response_model=list[RecipeResponse])
def get_recipes_by_meal_type(
    meal_type: str, 
    db: Session = Depends(get_db)
):
    return crud.get_recipes_by_meal_type(db, meal_type=meal_type)

@router.get("/list-by-diet-type/{diet_type}", response_model=list[RecipeResponse])
def get_recipes_by_diet_type(
    diet_type: str, 
    db: Session = Depends(get_db)
):
    return crud.get_recipes_by_diet_type(db, diet_type=diet_type)