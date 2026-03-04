from app.database import SessionLocal
from app.services.plan import PlanService
from app.schemas.plan import PlanResponse

from langchain.tools import tool

@tool
def get_current_plan_summary(user_id: int):
    """
    Displays the user's ACTIVE weekly nutritional plan with all scheduled meals.
    
    WHEN TO USE:
    - When the user asks about their current plan, weekly menu, or scheduled meals
    - When they say: "my plan", "view plan", "what do I have today", "my meals", "week's menu"
    - Before suggesting changes to the plan (to know the current state)
    
    WHEN NOT TO USE:
    - To search for new recipes outside the plan (use search_recipes_by_criteria)
    - To view the user's profile (use get_user_profile_summary)
    
    Returns: summary of the plan with meals per day, or indicates if there is no active plan.
    """
    db = SessionLocal()
    try:
        current_plan = PlanService.get_current_plan(db, user_id)
        
        if not current_plan:
            return "You don't have an active plan at the moment. Would you like me to generate one?"
        
        summary = _create_plan_summary(current_plan)

        # mode='json' ensures datetime is serialized as ISO string
        plan_data = PlanResponse.model_validate(current_plan).model_dump(mode='json')
        
        return {
            "result": summary,
            "plan": plan_data,
        }
        
    except Exception as e:
        return f"Error getting plan: {str(e)}"
    finally:
        db.close()

def _create_plan_summary(current_plan) -> str:
    """Creates a readable summary of the plan using the object directly"""
    
    # Day mapping (1 = Monday in the schema)
    DAYS_MAP = {
        1: "Monday",
        2: "Tuesday", 
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    
    # Meal type mapping
    MEAL_TYPE_MAP = {
        "breakfast": "Breakfast",
        "lunch": "Lunch", 
        "dinner": "Dinner",
        "snack": "Snack"
    }
    
    # Schedule mapping (simplified)
    SCHEDULE_MAP = {
        1: "1",
        2: "2", 
        3: "3",
        4: "4",
        5: "5",
        6: "6"
    }
    
    daily_menus = current_plan.daily_menus
    
    if not daily_menus:
        return "Your plan is active but has no assigned daily menus."
    
    # Sort by day of week
    daily_menus.sort(key=lambda x: x.day_of_week)
    
    # Overall statistics
    total_meals = sum(len(menu.meal_details) for menu in daily_menus)
    active_plan = "Active" if current_plan.active else "❌ Inactive"
    
    summary = f"**Your nutritional plan summary**\n\n"
    summary += f"Status: {active_plan}\n"
    summary += f"Duration: {len(daily_menus)} days\n"
    summary += f"Total meals: {total_meals}\n"
    summary += f"Plan ID: {current_plan.id}\n\n"
    
    # Daily details
    summary += "**Weekly distribution:**\n"
    
    # Accumulators for statistics
    weekly_stats = {
        'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0,
        'meals_count': 0, 'days_with_meals': 0
    }
    
    for menu in daily_menus:
        day_num = menu.day_of_week
        day_name = DAYS_MAP.get(day_num, f"Day {day_num}")
        meals = menu.meal_details
        
        if meals:
            weekly_stats['days_with_meals'] += 1
        
        summary += f"\n**{day_name}**\n"
        
        # Sort meals by schedule
        meals.sort(key=lambda x: x.schedule)
        
        # Show each meal
        for meal in meals:
            recipe = meal.recipe
            
            # Nutritional information
            calories = recipe.calories
            protein = recipe.protein
            carbs = recipe.carbs
            fat = recipe.fat
            
            # Accumulate statistics
            weekly_stats['calories'] += calories
            weekly_stats['protein'] += protein
            weekly_stats['carbs'] += carbs
            weekly_stats['fat'] += fat
            weekly_stats['meals_count'] += 1
            
            # Use meal.schedule directly as numeric key
            schedule_text = SCHEDULE_MAP.get(meal.schedule, str(meal.schedule))
            
            # Recipe information
            summary += f"{schedule_text}\n"
            summary += f"{recipe.name}\n"
            summary += f"- {calories} kcal {protein}g prot {carbs}g carb {fat}g fat\n"
            
            # Links if they exist
            if recipe.recipe_url or recipe.image_url:
                url = recipe.recipe_url or recipe.image_url
                summary += f"[View recipe]({url})\n"
            
            # Add separator between meals for better readability
            if meal != meals[-1]:  # If not the last meal
                summary += "---\n"
        
        # If no meals for this day
        if not meals:
            summary += f"No meals assigned\n"
    
    return summary