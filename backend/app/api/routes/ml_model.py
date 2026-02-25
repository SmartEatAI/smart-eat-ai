
from app.api.deps import get_current_user
from app.models.user import User
from app.models.plan import Plan
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from app.core.recommender import recommend_recipes, swap_for_similar

router = APIRouter(prefix="/ml", tags=["ML Recommender"])


class SwapRequest(BaseModel):
    recipe_id: int
    recommended_diets: List[str]
    selected_extra: Optional[List[str]] = []
    exclude_ids: Optional[List[int]] = []

@router.post("/recommend")
def recommend_endpoint(current_user: User = Depends(get_current_user)):
    profile = current_user.profile
    if profile is None:
        raise HTTPException(status_code=400, detail="User profile not found.")
    plan = current_user.plans[0] if current_user.plans else None
    if plan is None:
        raise HTTPException(status_code=400, detail="User plan not found.")
    meals_per_day = profile.meals_per_day
    macros = {
        "calories": profile.calories_target,
        "fat_content": profile.fat_target,
        "carbohydrate_content": profile.carbs_target,
        "protein_content": profile.protein_target
    }
    # Get diets from plan relationship
    diets = [dt.name for dt in plan.diet_types] if hasattr(plan, "diet_types") else []
    # Get used recipe ids from plan relationship
    used_ids = [r.id for r in plan.recipes] if hasattr(plan, "recipes") else []
    recipes = recommend_recipes(
        {k: v / meals_per_day for k, v in macros.items()},
        diets,
        meals_per_day,
        used_ids=set(used_ids)
    )
    return {"recipes": recipes.to_dict(orient="records")}

# Swap endpoint

@router.post("/swap-recipe")
def swap_recipe(data: SwapRequest):
    from app.models.recipe import Recipe
    from app.core.recommender import swap_for_similar
    from app.core.database import SessionLocal
    db = SessionLocal()
    recipe = db.query(Recipe).filter(Recipe.id == data.recipe_id).first()
    if recipe is None:
        db.close()
        raise HTTPException(status_code=404, detail="Recipe not found")
    # Infer meal label from recipe's meal_types
    meal_types = [mt.name for mt in recipe.meal_types]
    if not meal_types:
        db.close()
        raise HTTPException(status_code=400, detail="Recipe has no meal types")
    # Use the first meal type (or adapt as needed)
    meal_label = meal_types[0]
    new_recipe = swap_for_similar(
        recipe_id=data.recipe_id,
        meal_label=meal_label,
        recommended_diets=data.recommended_diets,
        selected_extra=data.selected_extra,
        exclude_ids=set(data.exclude_ids)
    )
    db.close()
    if new_recipe is None:
        raise HTTPException(
            status_code=404,
            detail="No similar recipe found for this meal type"
        )
    return new_recipe