from app.database import SessionLocal
from app.services.plan import PlanService
from app.services.meal_detail import MealDetailService
from app.schemas.plan import PlanResponse
from app.models.user import User
from app.models.recipe import Recipe
from app.models.plan import Plan
from typing import Optional
import logging

from langchain.tools import tool
from .constants import (
    DAYS_MAP as DAYS_MAP_ES,
    MEAL_TYPE_MAP as MEAL_TYPE_MAP_ES,
    get_meal_type_value as _get_meal_type_value
)

logger = logging.getLogger(__name__)


@tool
def replace_meal_in_plan(
    user_id: int, 
    new_recipe_id: Optional[int] = None,
    new_recipe_name: Optional[str] = None,
    meal_detail_id: Optional[int] = None,
    day_of_week: Optional[str] = None,
    meal_type: Optional[str] = None
):
    """
    Executes the replacement of a meal in the active plan. This is STEP 2 of the change flow.
    
    MANDATORY PREREQUISITE:
    ALWAYS call suggest_recipe_alternatives FIRST to show options to the user.
    NEVER call directly without the user having chosen an alternative.
    
    WHEN TO USE:
    - AFTER suggest_recipe_alternatives showed alternatives
    - AFTER the user chose an option (by name or number)
    
    WHEN NOT TO USE:
    - When the user says "change X" → first use suggest_recipe_alternatives
    - Without user confirmation about which alternative they prefer
    
    IDENTIFY THE MEAL TO REPLACE (one option):
    - day_of_week + meal_type: "monday" + "breakfast" (preferred)
    - meal_detail_id: ID from suggest_recipe_alternatives
    
    IDENTIFY THE NEW RECIPE (one option):
    - new_recipe_name: name of the chosen recipe (preferred when the user says the name)
    - new_recipe_id: numeric ID from alternatives_data
    
    EXAMPLES:
    - User says "option 1 which is Kumara salad":
      → replace_meal_in_plan(user_id=X, day_of_week="monday", meal_type="breakfast", new_recipe_name="Kumara salad")
    - User says "I want number 2":
      → identify the name of option 2 and use new_recipe_name
    
    Returns: change confirmation and updated plan.
    """
    db = SessionLocal()
    try:
        # Get user and validate
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"result": "User not found", "plan": None}
        
        # RESOLVE THE NEW RECIPE
        new_recipe = None
        
        # Option 1: By recipe_id (dataset ID)
        if new_recipe_id:
            new_recipe = db.query(Recipe).filter(Recipe.recipe_id == new_recipe_id).first()
            if not new_recipe:
                # Also try by internal id
                new_recipe = db.query(Recipe).filter(Recipe.id == new_recipe_id).first()
        
        # Option 2: By recipe name (case-insensitive partial search)
        if not new_recipe and new_recipe_name:
            recipe_name_lower = new_recipe_name.lower().strip()
            # Try exact match first
            new_recipe = db.query(Recipe).filter(
                Recipe.name.ilike(recipe_name_lower)
            ).first()
            
            # If no exact match, try partial
            if not new_recipe:
                new_recipe = db.query(Recipe).filter(
                    Recipe.name.ilike(f"%{recipe_name_lower}%")
                ).first()
            
            if not new_recipe:
                return {
                    "result": f"I couldn't find a recipe named '{new_recipe_name}'",
                    "plan": None
                }
        
        if not new_recipe:
            return {
                "result": "You must provide either new_recipe_id OR new_recipe_name to indicate the new recipe",
                "plan": None
            }
        
        # Check user's dietary restrictions
        if user.profile and user.profile.diet_types:
            user_diets = {d.name.lower() for d in user.profile.diet_types}
            recipe_diets = {d.name.lower() for d in new_recipe.diet_types}
            
            # The recipe must include at least one of the user's diets
            if user_diets and not user_diets.intersection(recipe_diets):
                return {
                    "result": f"This recipe does not comply with your dietary restrictions ({', '.join(user_diets)})",
                    "plan": None
                }
        
        # RESOLVE THE MEAL_DETAIL_ID
        target_meal_detail_id = meal_detail_id
        
        # If meal_detail_id is not provided, find it by day and meal type
        if not target_meal_detail_id and day_of_week and meal_type:
            # Normalize day
            day_normalized = DAYS_MAP_ES.get(day_of_week.lower().strip())
            if not day_normalized:
                return {"result": f"Day '{day_of_week}' not recognized", "plan": None}
            
            # Normalize meal type
            meal_type_normalized = MEAL_TYPE_MAP_ES.get(meal_type.lower().strip())
            if not meal_type_normalized:
                return {"result": f"Meal type '{meal_type}' not recognized", "plan": None}
            
            # Get active plan
            plan = db.query(Plan).filter(
                Plan.user_id == user_id,
                Plan.active.is_(True)
            ).first()
            
            if not plan:
                return {"result": "You don't have an active plan", "plan": None}
            
            # Find the meal_detail
            for dm in plan.daily_menus:
                if dm.day_of_week == day_normalized:
                    for md in dm.meal_details:
                        md_meal_type = _get_meal_type_value(md.meal_type)
                        if md_meal_type == meal_type_normalized:
                            target_meal_detail_id = md.id
                            break
                    break
            
            if not target_meal_detail_id:
                return {
                    "result": f"I couldn't find {meal_type} for {day_of_week} in your plan",
                    "plan": None
                }
        
        if not target_meal_detail_id:
            return {
                "result": "You must provide either meal_detail_id OR (day_of_week + meal_type) to identify which meal to replace",
                "plan": None
            }
        
        # Update using the existing service
        # Note: update_meal_detail_recipe_id expects the dataset recipe_id
        updated_meal = MealDetailService.update_meal_detail_recipe_id(
            db, 
            target_meal_detail_id, 
            new_recipe.recipe_id
        )
        
        if not updated_meal:
            return {"result": "Could not update the meal", "plan": None}
        
        # Get updated plan
        current_plan = PlanService.get_current_plan(db, user_id)
        if current_plan:
            # mode='json' ensures datetime is serialized as ISO string
            plan_response = PlanResponse.model_validate(current_plan).model_dump(mode='json')
            
            return {
                "result": f"✅ Meal successfully replaced with **{new_recipe.name}** ({new_recipe.calories} kcal, {new_recipe.protein}g protein)",
                "plan": plan_response,
                "new_recipe": {
                    "name": new_recipe.name,
                    "calories": new_recipe.calories,
                    "protein": new_recipe.protein,
                    "carbs": new_recipe.carbs,
                    "fat": new_recipe.fat
                }
            }
        else:
            return {
                "result": f"✅ Meal replaced with {new_recipe.name}, but no active plan found to display",
                "plan": None
            }
            
    except Exception as e:
        db.rollback()
        logger.error(f"Error in replace_meal_in_plan: {str(e)}")
        return {"result": f"Error replacing meal: {str(e)}", "plan": None}
    finally:
        db.close()