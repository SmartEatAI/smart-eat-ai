from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel, field_validator, Field

from schemas.user import UserInput
from core.recommender import recommend_recipes, swap_for_similar

router = APIRouter(prefix="/auth", tags=["Authentication"])

class SwapRequest(BaseModel):
    recipe_id: int
    meal_label: str
    recommended_diets: List[str]
    selected_extra: Optional[List[str]] = []
    exclude_ids: Optional[List[int]] = []

@router.post("/generate-plan")
def generate_plan(user: UserInput):

    bodyfat = estimate_bodyfat(user.sex, user.body_type)

    macros = calculate_macros(
        user.sex,
        user.age,
        user.height,
        user.weight,
        bodyfat,
        user.activity,
        user.goal
    )

    meals = user.meals_per_day

    recipes = recommend_recipes(
        {
            "calories": macros["calories"]/meals,
            "fat_content": macros["fat"]/meals,
            "carbohydrate_content": macros["carbs"]/meals,
            "protein_content": macros["protein"]/meals
        },
        user.diets,
        meals
    )

    return {
        "macros": macros,
        "recipes": recipes.to_dict(orient="records")
    }
    
@router.post("/swap-recipe")
def swap_recipe(data: SwapRequest):

    new_recipe = swap_for_similar(
        recipe_id=data.recipe_id,
        meal_label=data.meal_label,
        recommended_diets=data.recommended_diets,
        selected_extra=data.selected_extra,
        exclude_ids=set(data.exclude_ids)
    )

    if new_recipe is None:
        raise HTTPException(
            status_code=404,
            detail="No similar recipe found for this meal type"
        )

    return new_recipe