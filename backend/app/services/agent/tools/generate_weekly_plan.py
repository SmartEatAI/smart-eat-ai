from langchain.tools import tool
from sqlalchemy import and_
from app.database import SessionLocal
from typing import List, Dict
import random

# Services / Models / Schemas
from app.services.profile import ProfileService
from app.services.plan import PlanService
from app.schemas.plan import PlanResponse, PlanCreate
from app.schemas.meal_detail import MealDetailBase
from app.schemas.daily_menu import DailyMenuCreate
from app.schemas.enums import MealTypeEnum
from app.models.recipe import Recipe
from app.models.diet_type import DietType
from app.models.meal_type import MealType
from app.schemas.recipe import RecipeResponse
from app.services.profile import ProfileService

# Functions
from app.core.recommender import get_meal_order

# LLM to ask whether it complies with restrictions
from app.core.config_ollama import llm  # Your ChatOllama instance



def meal_calories_distribution(n_meals: int):
    """
    Function to calculate the calorie distribution based on
    the number of daily meals.
    """
    mapping = {
        3: [0.3, 0.4, 0.3],
        4: [0.25, 0.3, 0.15, 0.3],
        5: [0.2, 0.1, 0.3, 0.1, 0.3],
        6: [0.2, 0.1, 0.25, 0.1, 0.25, 0.1]
    }
    return mapping.get(n_meals, mapping[3])

def calculate_calorie_ranges(calories_target: float, n_meals: int) -> Dict[str, Dict[str, float]]:
    """
    Calculates the calorie ranges for each meal type
    """
    # Maximum percentages per meal type
    calories_percents_max = {
        3: {"breakfast": 0.30, "lunch": 0.40, "dinner": 0.40},
        4: {"breakfast": 0.25, "lunch": 0.35, "snack": 0.10, "dinner": 0.35},
        5: {"breakfast": 0.25, "lunch": 0.35, "snack": 0.10, "dinner": 0.35},
        6: {"breakfast": 0.25, "lunch": 0.30, "snack": 0.10, "dinner": 0.30}
    }
    
    # Get the distribution for this number of meals
    max_percents = calories_percents_max.get(n_meals, calories_percents_max[3])
    meal_order = get_meal_order(n_meals)
    
    # Create dictionary with ranges per meal type
    calorie_ranges = {}
    for i, meal_type in enumerate(meal_order):
        max_percent = max_percents[meal_type] if meal_type in max_percents else 0.35
        min_percent = max_percent / 2  # Minimum is half of maximum
        
        calorie_ranges[meal_type] = {
            "min": calories_target * min_percent,
            "max": calories_target * max_percent
        }
    
    return calorie_ranges

def all_recipes_for_user(user_id: int, max_recipes_per_type: int = 50) -> Dict[str, List[RecipeResponse]]:
    """
    Gets all recipes that match the user's profile
    based on meal types, diets, and calorie ranges.
    """
    db = SessionLocal()
    
    try:
        # Get user profile
        profile = ProfileService.get_user_profile(db, user_id)
        
        if not profile:
            return {}
        
        # Calculate calorie ranges
        calorie_ranges = calculate_calorie_ranges(
            profile.calories_target, 
            profile.meals_per_day
        )
        
        # Filter by meal type without repeating
        meal_types = list(dict.fromkeys(get_meal_order(profile.meals_per_day)))
        
        # Get user's diet names
        diet_type_names = [diet_type.name for diet_type in profile.diet_types]
        
        # Results per meal type
        all_recipes = {}
        
        for meal_type_name in meal_types:
            # Base query
            query = db.query(Recipe).distinct()
            
            # Filter by meal type
            query = query.join(Recipe.meal_types).filter(
                MealType.name == meal_type_name
            ).distinct()
            
            # Filter by diet types (user may have multiple)
            if diet_type_names:
                query = query.join(Recipe.diet_types).filter(
                    DietType.name.in_(diet_type_names)
                ).distinct()
            
            # Filter by calorie range
            calorie_range = calorie_ranges.get(meal_type_name, {})
            if calorie_range:
                query = query.filter(
                    and_(
                        Recipe.calories >= calorie_range.get("min", 0),
                        Recipe.calories <= calorie_range.get("max", float('inf'))
                    )
                )
            
            # Execute query and get results
            recipes = query.all()

            random.shuffle(recipes)
            print(f"Before AI filtering - {meal_type_name}: {len(recipes)} recipes")

            # If there are restrictions or diets, filter with AI
            if profile.restrictions or profile.diet_types:
                # Get user's restriction names
                if profile.restrictions:
                    restrictions_names = [restriction.name for restriction in profile.restrictions]
                    restrictions_text = ", ".join(restrictions_names)
                else:
                    restrictions_text = "none"

                # Check for vegan/vegetarian diets
                target_diets = {"vegan", "vegetarian"}

                # Filter the original list
                diet_type_names_filtered = [name.lower() for name in diet_type_names if name.lower() in target_diets]

                # Get user's diet names
                diet_text = ", ".join(diet_type_names_filtered)

                print(f"Filtering with AI (batch) - Restrictions: [{restrictions_text}], Diets: [{diet_text}]")
                
                # Usar validación en batch para reducir llamadas al LLM (evita rate limits de Groq)
                from .rate_limit_utils import validate_recipes_batch
                
                filtered_recipes = validate_recipes_batch(
                    llm=llm,
                    recipes=recipes[:max_recipes_per_type * 2],
                    restrictions_text=restrictions_text,
                    diet_text=diet_text,
                    batch_size=10  # 10 recetas por llamada al LLM
                )
                
                # Limitar al máximo necesario
                filtered_recipes = filtered_recipes[:max_recipes_per_type]
                
                print(f"After AI filtering (batch) - {meal_type_name}: {len(filtered_recipes)} valid recipes")
                
                # Use filtered recipes
                limited_recipes = filtered_recipes
                
            else:
                # Without AI filters, limit directly
                limited_recipes = recipes[:max_recipes_per_type]
                print(f"Without AI filters - {meal_type_name}: {len(limited_recipes)} recipes")
            
            # Convert to RecipeResponse
            recipes_response = []
            for recipe in limited_recipes:
                recipe_response = RecipeResponse.model_validate(recipe)
                recipes_response.append(recipe_response)
            
            all_recipes[meal_type_name] = recipes_response

            print(f"For {meal_type_name} there are {len(recipes)} matches.")
        
        return all_recipes
    
    finally:
        db.close()


@tool
def generate_weekly_plan(user_id: int):
    """
    Generates a complete weekly nutritional plan (7 days) personalized for the user.
    
    WHEN TO USE:
    - "Generate a plan", "I need a new plan", "create weekly plan"
    - "I want to start a nutritional plan", "make me a weekly menu"
    - When the user has no active plan and wants a new one
    - When they want to completely replace their current plan
    
    WHEN NOT TO USE:
    - To view the existing plan (use get_current_plan_summary)
    - To change a single meal (use suggest_recipe_alternatives + replace_meal_in_plan)
    - To search for specific recipes (use search_recipes_by_criteria)
    
    The plan is generated based on:
    - Dietary restrictions from the profile
    - Calculated calorie target
    - Configured number of daily meals
    - Saved tastes and preferences
    
    Returns: complete 7-day plan with all meals.
    """
    db = SessionLocal()

    try:
        # Get profile
        profile = ProfileService.get_user_profile(db, user_id)
        
        if not profile:
            return {
                "result": "No profile found for the user", 
                "plan": None
            }
        
        # Get meal order according to meals_per_day
        meal_order = get_meal_order(profile.meals_per_day)

        # Get available recipes using the new function
        recipes_by_meal_type = all_recipes_for_user(user_id)
        
        # Check if there are available recipes
        if not recipes_by_meal_type or not any(recipes_by_meal_type.values()):
            return {
                "result": "No recipes available that meet the restrictions and calorie ranges", 
                "plan": None
            }
        
        # Calculate calorie distribution per meal
        calorie_distribution = meal_calories_distribution(profile.meals_per_day)
        
        # Create distribution mapping by meal type
        meal_calorie_distribution = {}
        for i, meal_label in enumerate(meal_order):
            if i < len(calorie_distribution):
                meal_calorie_distribution[meal_label] = calorie_distribution[i]
        
        # Calculate calorie ranges for reference
        calorie_ranges = calculate_calorie_ranges(profile.calories_target, profile.meals_per_day)
        
        # Dictionary to keep track of used recipes per day
        used_recipe_ids = {}
        
        # List to store all daily_menus for the plan
        daily_menus_data = []
        
        # Generate daily menus
        for day in range(1, 8):  # 7 days
            # List to store the meal_details for this day
            meal_details_for_day = []
            
            # For each meal of the day
            for meal_idx, meal_label in enumerate(meal_order):
                # Calculate target calories for this meal using the distribution
                target_calories = profile.calories_target * meal_calorie_distribution.get(meal_label, 0.25)
                
                # Get candidate recipes for this meal type
                candidates = recipes_by_meal_type.get(meal_label, [])
                
                if candidates:
                    # Filter recipes not used recently
                    available_candidates = []
                    for recipe_response in candidates:
                        recipe_id = recipe_response.id
                        
                        # Check if the recipe was used in the last 6 days
                        if recipe_id in used_recipe_ids:
                            days_since_used = day - used_recipe_ids[recipe_id]
                            if days_since_used <= 6:
                                continue
                        
                        # Check that it meets the calorie range
                        recipe_calories = recipe_response.calories
                        calorie_range = calorie_ranges.get(meal_label, {})
                        
                        min_calories = calorie_range.get('min', target_calories * 0.7)
                        max_calories = calorie_range.get('max', target_calories * 1.3)
                        
                        if min_calories <= recipe_calories <= max_calories:
                            available_candidates.append(recipe_response)
                    
                    if available_candidates:
                        # Choose the one closest to the target calories
                        selected_recipe = min(available_candidates, 
                            key=lambda r: abs(r.calories - target_calories))
                        
                        selected_recipe_id = selected_recipe.id
                        
                        # Register recipe usage
                        used_recipe_ids[selected_recipe_id] = day
                        
                        # Create MealDetailBase
                        meal_detail_data = MealDetailBase(
                            recipe_id=selected_recipe_id,
                            schedule=meal_idx + 1,
                            status=0,  # 0: pending
                            meal_type=MealTypeEnum(meal_label)  # Convert string to Enum
                        )
                        
                        meal_details_for_day.append(meal_detail_data)
            
            # Create DailyMenuCreate with all meal_details of the day
            if meal_details_for_day or len(meal_details_for_day) == profile.meals_per_day:  # Only create if there are meals for the day
                daily_menu_data = DailyMenuCreate(
                    plan_id=0,  # This value will be ignored/overwritten in the CRUD
                    day_of_week=day,
                    meal_details=meal_details_for_day
                )
                
                daily_menus_data.append(daily_menu_data)
        
        # Check if any menu could be generated
        if not daily_menus_data or len(daily_menus_data) != 7:
            return {
                "result": "Could not generate a plan. There are not enough recipes available that meet the restrictions and calorie ranges.", 
                "plan": None
            }
        
        # Create the PlanCreate object with all daily_menus
        plan_create_data = PlanCreate(
            daily_menus=daily_menus_data
        )
        
        # Create the plan using the service
        new_plan = PlanService.create_plan(db, plan_create_data, user_id)
        
        # Get complete plan with all details
        complete_plan = PlanService.get_current_plan(db, user_id)
        # mode='json' ensures datetime is serialized as ISO string
        plan_response = PlanResponse.model_validate(complete_plan).model_dump(mode='json')
        
        # Prepare summary with recipe information
        recipes_found_summary = {}
        for meal, recipes in recipes_by_meal_type.items():
            if recipes:
                recipes_found_summary[meal] = len(recipes)
        
        return {
            "result": f"✅ Weekly plan generated successfully.",
        }
        
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return {"result": f"Error generating plan: {str(e)}", "plan": None}
    finally:
        db.close()