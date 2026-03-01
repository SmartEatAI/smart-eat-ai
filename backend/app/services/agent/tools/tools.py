from .buscar_en_base_datos import buscar_en_base_datos
from .search_recipes_by_criteria import search_recipes_by_criteria
from .generate_weekly_plan import generate_weekly_plan
from .update_user_preference import update_user_preference
from .suggest_recipe_alternatives import suggest_recipe_alternatives
from .replace_meal_in_plan import replace_meal_in_plan
from .get_user_profile_summary import get_user_profile_summary
from .get_current_plan_summary import get_current_plan_summary

# Actualizar lista de herramientas disponibles
nutrition_tools = [
    buscar_en_base_datos,
    search_recipes_by_criteria,
    generate_weekly_plan,
    update_user_preference,
    suggest_recipe_alternatives,
    replace_meal_in_plan,
    get_user_profile_summary,
    get_current_plan_summary
]