from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from langchain.tools import tool
import logging

from app.database import SessionLocal
from app.models.recipe import Recipe
from app.models.user import User
from app.models.plan import Plan
from app.core.config_ollama import llm


@tool
def search_recipes_by_criteria(
    user_id: int,
    meal_type: Optional[str] = None,
    diet_type: Optional[str] = None,
    max_calories: Optional[float] = None,
    min_protein: Optional[float] = None,
    max_carbs: Optional[float] = None,
    max_fat: Optional[float] = None,
    query: Optional[str] = None
):
    """
    Searches for recipes in the GENERAL DATABASE according to specific criteria. NOT related to the active plan.
    
    WHEN TO USE (general recipe searches):
    - "Search for chicken recipes", "vegan recipes", "low-calorie options"
    - "Give me high-protein recipes", "breakfast recipes"
    - When the user wants to EXPLORE new recipes WITHOUT modifying their plan
    - When they ask for general recommendations or meal ideas
    
    WHEN NOT TO USE (use suggest_recipe_alternatives instead):
    - "I want to change Monday's breakfast" → suggest_recipe_alternatives
    - "Change Sunday's dinner" → suggest_recipe_alternatives  
    - Any request to MODIFY a meal from the active plan
    
    KEY DIFFERENCE: This tool searches the entire database.
    suggest_recipe_alternatives searches for SIMILAR alternatives to a specific meal from the plan.
    
    Parameters:
    - meal_type: breakfast, lunch, dinner, snack
    - diet_type: vegetarian, vegan, gluten-free, etc.
    - max_calories, min_protein, max_carbs, max_fat: nutritional filters
    - query: semantic search by ingredients or description
    
    Returns 5 recipes by default.
    """
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return {"result": "User or profile not found", "recipes": []}

        profile = user.profile

        # Only strictly filter by vegan/vegetarian diets (same as in generate_weekly_plan)
        # Other diets like "high protein" should not exclude recipes
        target_strict_diets = {"vegan", "vegetarian"}
        required_diets = set()
        if profile.diet_types:
            for d in profile.diet_types:
                if d.name.lower() in target_strict_diets:
                    required_diets.add(d.name.lower())

        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user.id, Plan.active.is_(True))
            .first()
        )
        exclude_ids = (
            {
                meal.recipe_id 
                for day in plan.daily_menus 
                for meal in day.meal_details
            }
            if plan else set()
        )

        query_db = db.query(Recipe)
        if meal_type:
            query_db = query_db.join(Recipe.meal_types).filter(
                Recipe.meal_types.any(
                    name=meal_type.lower()
                )
            )
        if diet_type:
            query_db = query_db.join(Recipe.diet_types).filter(
                Recipe.diet_types.any(
                    name=diet_type.lower()
                )
            )
        recipes = query_db.all()
        logging.info(f"Total recipes after meal_type/diet_type filter: {len(recipes)}")

        # Nutritional and diet filtering
        filtered_recipes: List[Recipe] = []
        for recipe in recipes:
            if recipe.recipe_id in exclude_ids:
                continue
            recipe_diets = {d.name.lower() for d in recipe.diet_types}
            if required_diets and not required_diets.intersection(recipe_diets):
                continue
            if max_calories is not None and recipe.calories > max_calories:
                continue
            if min_protein is not None and recipe.protein < min_protein:
                continue
            if max_carbs is not None and recipe.carbs > max_carbs:
                continue
            if max_fat is not None and recipe.fat > max_fat:
                continue
            filtered_recipes.append(recipe)
        logging.info(f"Recipes after nutritional filter: {len(filtered_recipes)}")

        # AI filtering for dietary restrictions
        use_llm_filter = False
        restrictions_text = ""
        diet_text = ""
        
        if profile.restrictions or profile.diet_types:
            # Get user restriction names
            restriction_names = [r.name for r in profile.restrictions] if profile.restrictions else []
            restrictions_text = ", ".join(restriction_names)
            
            # Check for vegan/vegetarian diets
            diet_type_names = [d.name for d in profile.diet_types] if profile.diet_types else []
            target_diets = {"vegan", "vegetarian"}
            diet_text_list = [name for name in diet_type_names if name.lower() in target_diets]
            diet_text = ", ".join(diet_text_list)
            
            # Activate LLM filter if there are restrictions or vegan/vegetarian diets
            if restriction_names or diet_text_list:
                use_llm_filter = True
                logging.info(f"Applying AI filter (batch) - Restrictions: [{restrictions_text}], Diets: [{diet_text}]")
        
        if use_llm_filter:
            # Usar validación en batch para reducir llamadas al LLM (evita rate limits de Groq)
            from .rate_limit_utils import validate_recipes_batch
            
            filtered_recipes = validate_recipes_batch(
                llm=llm,
                recipes=filtered_recipes,
                restrictions_text=restrictions_text,
                diet_text=diet_text,
                batch_size=10  # 10 recetas por llamada al LLM
            )
            
            logging.info(f"Recipes after AI filter (batch): {len(filtered_recipes)}")

        # Text search in name and ingredients (normal SQL search)
        if query:
            query_lower = query.lower()
            filtered_recipes = [
                r for r in filtered_recipes 
                if query_lower in r.name.lower() or 
                    (r.ingredients and query_lower in r.ingredients.lower())
            ]
            logging.info(f"Recipes after query filter '{query}': {len(filtered_recipes)}")

        response = [
            f"Name: {r.name}, protein: {r.protein}, carbs: {r.carbs}, fat: {r.fat}"
            for r in filtered_recipes[:5]
        ]

        # If no exact recipes, show close suggestions
        if not response and min_protein is not None:
            close_recipes = [
                r for r in recipes
                if r.protein >= min_protein * 0.8 and r.recipe_id not in exclude_ids
            ]
            close_response = [
                f"Name: {r.name}, protein: {r.protein}, carbs: {r.carbs}, fat: {r.fat}"
                for r in close_recipes[:5]
            ]
            if close_response:
                return {
                    "result": f"No recipes found with exactly {min_protein}g of protein, but here are close options:",
                    "recipes": close_response
                }
            else:
                return {
                    "result": f"No recipes found matching the requested criteria.",
                    "recipes": []
                }

        return {
            "result": f"Found {len(response)} recipes",
            "recipes": response
        }

    except Exception as e:
        logging.error(f"Error searching recipes: {str(e)}")
        db.rollback()
        return {
            "result": f"Error searching recipes: {str(e)}", 
            "recipes": []
        }
    finally:
        db.close()