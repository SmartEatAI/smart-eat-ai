
from app.api.deps import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.recommender import swap_for_similar
from app.database import get_db

router = APIRouter(prefix="/ml", tags=["ML Recommender"])

@router.post("/swap-recipe")
def swap_recipe(
    recipe_id: int,
    meal_label: str,
    n_search: int = 550,
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db) 
):
    new_recipe = swap_for_similar(
        db=db,
        user=user,
        recipe_id=recipe_id,
        meal_label=meal_label,
        n_search=n_search
    )
    if new_recipe is None:
        raise HTTPException(
            status_code=404,
            detail="No similar recipe found for this meal type"
        )
    return new_recipe
