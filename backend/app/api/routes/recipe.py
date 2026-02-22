from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.recipe import RecipeResponse
from app.crud import recipe as crud

router = APIRouter(prefix="/recipe")
@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe_by_id(
    recipe_id: int, 
    db: Session = Depends(get_db)
):
    
    recipe = crud.get_recipe_by_id(db, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return recipe

@router.get("/list-by-meal-type/{meal_type_id}", response_model=List[RecipeResponse])
def get_recipes_by_meal_type(
    meal_type_id: int, 
    db: Session = Depends(get_db)
):
    recipes = crud.get_recipes_by_meal_type(db, meal_type_id=meal_type_id)
    if not recipes:
        raise HTTPException(status_code=404, detail="No se encontraron recetas para este tipo de comida")
    return recipes

@router.get("/list-by-diet-type/{diet_type_id}", response_model=List[RecipeResponse])
def get_recipes_by_diet_type(
    diet_type_id: int, 
    db: Session = Depends(get_db)
):
    recipes = crud.get_recipes_by_diet_type(db, diet_type_id=diet_type_id)
    if not recipes:
        raise HTTPException(status_code=404, detail="No se encontraron recetas para este tipo de dieta")
    return recipes