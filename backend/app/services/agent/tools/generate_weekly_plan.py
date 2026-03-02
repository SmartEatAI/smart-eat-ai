from langchain.tools import tool
from sqlalchemy import and_
from app.database import SessionLocal
from typing import List, Dict
import random

# Servicios / Modelos / Esquemas
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

# Funciones
from app.core.recommender import get_meal_order



def meal_calories_distribution(n_meals: int):
    """
    Funcion para calcular la distribucion de calorias según 
    la cantidad de comidas diarias.

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
    Calcula los rangos de calorías para cada tipo de comida
    """
    # Porcentajes máximos por tipo de comida
    calories_percents_max = {
        3: {"breakfast": 0.30, "lunch": 0.40, "dinner": 0.40},
        4: {"breakfast": 0.25, "lunch": 0.35, "snack": 0.10, "dinner": 0.35},
        5: {"breakfast": 0.25, "lunch": 0.35, "snack": 0.10, "dinner": 0.35},
        6: {"breakfast": 0.25, "lunch": 0.30, "snack": 0.10, "dinner": 0.30}
    }
    
    # Obtener la distribución para este número de comidas
    max_percents = calories_percents_max.get(n_meals, calories_percents_max[3])
    meal_order = get_meal_order(n_meals)
    
    # Crear diccionario con rangos por tipo de comida
    calorie_ranges = {}
    for i, meal_type in enumerate(meal_order):
        max_percent = max_percents[meal_type] if meal_type in max_percents else 0.35
        min_percent = max_percent / 2  # El mínimo es la mitad del máximo
        
        calorie_ranges[meal_type] = {
            "min": calories_target * min_percent,
            "max": calories_target * max_percent
        }
    
    return calorie_ranges

def all_recipes_for_user(user_id: int,  max_recipes_per_type: int = 50) -> Dict[str, List[RecipeResponse]]:
    """
    Obtiene todas las recetas que coinciden con el perfil del usuario
    basado en tipos de comida, dietas y rangos de calorías.
    """
    db = SessionLocal()
    
    try:
        # Obtener perfil de usuario
        profile = ProfileService.get_user_profile(db, user_id)
        
        if not profile:
            return {}
        
        # Calcular rangos de calorías
        calorie_ranges = calculate_calorie_ranges(
            profile.calories_target, 
            profile.meals_per_day
        )
        
        # Filtro por tipo de comida sin repetir
        meal_types = list(dict.fromkeys(get_meal_order(profile.meals_per_day)))
        
        # Obtener nombres de dietas del usuario
        diet_type_names = [diet_type.name for diet_type in profile.diet_types]
        
        # Resultados por tipo de comida
        all_recipes = {}
        
        for meal_type_name in meal_types:
            # Consulta base
            query = db.query(Recipe).distinct()
            
            # Filtrar por tipo de comida
            query = query.join(Recipe.meal_types).filter(
                MealType.name == meal_type_name
            ).distinct()
            
            # Filtrar por tipos de dieta (el usuario puede tener múltiples)
            if diet_type_names:
                query = query.join(Recipe.diet_types).filter(
                    DietType.name.in_(diet_type_names)
                ).distinct()
            
            # Filtrar por rango de calorías
            calorie_range = calorie_ranges.get(meal_type_name, {})
            if calorie_range:
                query = query.filter(
                    and_(
                        Recipe.calories >= calorie_range.get("min", 0),
                        Recipe.calories <= calorie_range.get("max", float('inf'))
                    )
                )
            
            # Ejecutar consulta y obtener resultados
            recipes = query.all()

            random.shuffle(recipes)

            # Limitar a max_recipes_per_type para tener variedad
            limited_recipes = recipes[:max_recipes_per_type]
            
            # Convertir a RecipeResponse
            recipes_response = []
            for recipe in limited_recipes:
                recipe_response = RecipeResponse.model_validate(recipe)
                recipes_response.append(recipe_response)
            
            all_recipes[meal_type_name] = recipes_response

            print(f"Para {meal_type_name} hay {len(recipes)} coincidencias.")
        
        return all_recipes
    
    finally:
        db.close()



@tool
def generate_weekly_plan(user_id: int):
    """
    Genera un plan nutricional semanal personalizado basado en el perfil del usuario.
    Utiliza el perfil para calcular macros y selecciona recetas apropiadas.
    """

    db = SessionLocal()

    try:
        # Obtener perfil
        profile = ProfileService.get_user_profile(db, user_id)
        
        if not profile:
            return {
                "result": "No se encontró perfil para el usuario", 
                "plan": None
            }
        
        # Obtener orden de comidas según meals_per_day
        meal_order = get_meal_order(profile.meals_per_day)

        # Obtener recetas disponibles usando la nueva función
        recipes_by_meal_type = all_recipes_for_user(user_id)
        
        # Verificar si hay recetas disponibles
        if not recipes_by_meal_type or not any(recipes_by_meal_type.values()):
            return {
                "result": "No hay recetas disponibles que cumplan con las restricciones y rangos calóricos", 
                "plan": None
            }
        
        # Calcular distribución de calorías por comida
        calorie_distribution = meal_calories_distribution(profile.meals_per_day)
        
        # Crear mapeo de distribución por tipo de comida
        meal_calorie_distribution = {}
        for i, meal_label in enumerate(meal_order):
            if i < len(calorie_distribution):
                meal_calorie_distribution[meal_label] = calorie_distribution[i]
        
        # Calcular rangos de calorías para referencia
        calorie_ranges = calculate_calorie_ranges(profile.calories_target, profile.meals_per_day)
        
        # Diccionario para llevar control de recetas usadas por tipo
        used_recipe_ids = {}
        
        # Lista para almacenar todos los daily_menus del plan
        daily_menus_data = []
        
        # Generar menús diarios
        for day in range(1, 8):  # 7 días
            # Lista para almacenar los meal_details de este día
            meal_details_for_day = []
            
            # Para cada comida del día
            for meal_idx, meal_label in enumerate(meal_order):
                # Calcular calorías objetivo para esta comida usando la distribución
                target_calories = profile.calories_target * meal_calorie_distribution.get(meal_label, 0.25)
                
                # Obtener recetas candidatas para este tipo de comida
                candidates = recipes_by_meal_type.get(meal_label, [])
                
                if candidates:
                    # Filtrar recetas no usadas recientemente
                    available_candidates = []
                    for recipe_response in candidates:
                        recipe_id = recipe_response.id
                        
                        # Verificar si la receta ya se usó en los ultimos 3 dias
                        if recipe_id in used_recipe_ids:
                            days_since_used = day - used_recipe_ids[recipe_id]
                            if days_since_used <= 6:
                                continue
                        
                        # Verificar que cumpla con el rango de calorías
                        recipe_calories = recipe_response.calories
                        calorie_range = calorie_ranges.get(meal_label, {})
                        
                        min_calories = calorie_range.get('min', target_calories * 0.7)
                        max_calories = calorie_range.get('max', target_calories * 1.3)
                        
                        if min_calories <= recipe_calories <= max_calories:
                            available_candidates.append(recipe_response)
                    
                    if available_candidates:
                        # Elegir el que más se acerque a las calorías objetivo
                        selected_recipe = min(available_candidates, 
                            key=lambda r: abs(r.calories - target_calories))
                        
                        selected_recipe_id = selected_recipe.id
                        
                        # Registrar uso de la receta
                        used_recipe_ids[selected_recipe_id] = day
                        
                        # Crear MealDetailBase
                        meal_detail_data = MealDetailBase(
                            recipe_id=selected_recipe_id,
                            schedule=meal_idx + 1,
                            status=0,  # 0: pending
                            meal_type=MealTypeEnum(meal_label)  # Convertir string a Enum
                        )
                        
                        meal_details_for_day.append(meal_detail_data)
            
            # Crear DailyMenuCreate con todos los meal_details del día
            if meal_details_for_day:  # Solo crear si hay comidas para el día
                daily_menu_data = DailyMenuCreate(
                    plan_id=0,  # Este valor se ignorará/sobrescribirá en el CRUD
                    day_of_week=day,
                    meal_details=meal_details_for_day
                )
                
                daily_menus_data.append(daily_menu_data)
        
        # Verificar si se pudo generar algún menú
        if not daily_menus_data:
            return {
                "result": "No se pudo generar un plan con las recetas disponibles", 
                "plan": None
            }
        
        # Crear el objeto PlanCreate con todos los daily_menus
        plan_create_data = PlanCreate(
            daily_menus=daily_menus_data
        )
        
        # Crear el plan usando el servicio
        new_plan = PlanService.create_plan(db, plan_create_data, user_id)
        
        # Obtener plan completo con todos los detalles
        complete_plan = PlanService.get_current_plan(db, user_id)
        plan_response = PlanResponse.model_validate(complete_plan).model_dump()
        
        # Preparar resumen con información de recetas
        recipes_found_summary = {}
        for meal, recipes in recipes_by_meal_type.items():
            if recipes:
                recipes_found_summary[meal] = len(recipes)
        
        return {
            "result": f"✅ Plan semanal generado exitosamente.",
            "plan": plan_response,
        }
        
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return {"result": f"Error generando plan: {str(e)}", "plan": None}
    finally:
        db.close()