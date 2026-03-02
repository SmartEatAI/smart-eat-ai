from langchain.tools import tool
from app.database import SessionLocal
from typing import List, Dict, Any

# Servicios / Modelos / Esquemas
from app.services.profile import ProfileService
from app.services.recipe import RecipeService
from app.services.plan import PlanService
from app.schemas.plan import PlanResponse, PlanCreate
from app.schemas.meal_detail import MealDetailBase
from app.schemas.daily_menu import DailyMenuCreate
from app.schemas.enums import MealTypeEnum
from app.config import settings

# Funciones
from app.core.recommender import get_meal_order
from app.utils.calculations import calculate_age

# Chroma / Embedding
from langchain_chroma import Chroma
from app.core.config_ollama import embeddings



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


def all_recipes_for_user(user_id: int) -> List[Dict[str, Any]]:
    """
    Obtiene todas las recetas que coinciden con el perfil del usuario
    basado en tipos de comida, dietas y rangos de calorías.
    """
    db = SessionLocal()

    # Obtener perfil de usuario
    profile = ProfileService.get_user_profile(db, user_id)

    # Calcular rangos de calorías
    calorie_ranges = calculate_calorie_ranges(
        profile.calories_target, 
        profile.meals_per_day
    )

    # Filtro por tipo de comida sin repetir
    meal_types = list(dict.fromkeys(get_meal_order(profile.meals_per_day)))

    # Filtro por tipo de dieta
    diet_type_names = [diet_type.name for diet_type in profile.diet_types]

    vector_db = Chroma(
        persist_directory=settings.CHROMA_DB,
        embedding_function=embeddings
    )

    # Resultados por tipo de comida
    all_recipes = {}

    for meal_type in meal_types:
            # Construir filtro de metadatos para este tipo de comida
            where_filter = {
                "$and": [
                    # Filtro por tipo de comida (exacto)
                    #{"meal_types": {"$eq": meal_type}},
                    
                    # Filtro por tipo de dieta (el usuario puede tener múltiples)
                    {"diet_types": {"$in": diet_type_names}},
                    
                    # Filtro por rango de calorías
                    #{
                    #    "$and": [
                    #        {"calories": {"$gte": calorie_ranges[meal_type]["min"]}},
                    #        {"calories": {"$lte": calorie_ranges[meal_type]["max"]}}
                    #    ]
                    #}
                ]
            }

    
            # Búsqueda semántica con filtros
            results = vector_db.similarity_search(
                query=f"{meal_type}",
                k=1000,  # Número de resultados por tipo de comida
                #filter=where_filter
            )

            # Procesar resultados
            recipes_for_meal = []
            for doc in results:
                recipes_for_meal.append({
                    "name": doc.page_content.split("Name: ")[1].split(". Diet")[0] if "Name:" in doc.page_content else doc.page_content,
                    "metadata": doc.metadata,
                    "content": doc.page_content
                })
            
            all_recipes[meal_type] = recipes_for_meal
            
            print(f"Para {meal_type} hay {len(all_recipes[meal_type])} coincidencias.")
    return all_recipes




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
        
        # Obtener orden de comidas según meals_per_day
        meal_order = get_meal_order(profile.meals_per_day)

        # Obtener recetas disponibles usando la nueva función
        recipes_by_meal_type = all_recipes_for_user(user_id)
        
         # Verificar si hay recetas disponibles
        if not any(recipes_by_meal_type.values()):
            return {
                "result": "No hay recetas disponibles que cumplan con las restricciones y rangos calóricos", 
                "plan": None
            }
        
        # Calcular distribución de calorías por comida usando meal_calories_distribution
        calorie_distribution = meal_calories_distribution(profile.meals_per_day)
        
        # Crear mapeo de distribución por tipo de comida
        meal_calorie_distribution = {}
        for i, meal_label in enumerate(meal_order):
            if i < len(calorie_distribution):
                meal_calorie_distribution[meal_label] = calorie_distribution[i]
        
        # Calcular rangos de calorías para referencia
        calorie_ranges = calculate_calorie_ranges(profile.calories_target, profile.meals_per_day)
        
        # Diccionario para llevar control de recetas usadas por tipo
        #used_recipe_ids = {}
        
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
                    # Filtrar recetas no usadas recientemente (últimos 3 días)
                    available_candidates = []
                    for recipe_data in candidates:
                        recipe_id = recipe_data['metadata'].get('id')
                        
                        # Verificar si la receta ya se usó en los últimos 3 días
                        #if recipe_id in used_recipe_ids.get(meal_label, {}):
                        #    days_since_used = day - used_recipe_ids[meal_label].get(recipe_id, 0)
                        #    if days_since_used <= 3:
                        #        continue
                        
                        # Verificar que cumpla con el rango de calorías
                        recipe_calories = recipe_data['metadata'].get('calories', 0)
                        calorie_range = calorie_ranges.get(meal_label, {})
                        
                        min_calories = calorie_range.get('min', target_calories * 0.7)
                        max_calories = calorie_range.get('max', target_calories * 1.3)
                        
                        if min_calories <= recipe_calories <= max_calories:
                            available_candidates.append(recipe_data)
                    
                    if available_candidates:
                        # Elegir el que más se acerque a las calorías objetivo
                        selected_recipe_data = min(available_candidates, 
                            key=lambda r: abs(r['metadata'].get('calories', 0) - target_calories))
                        
                        selected_recipe_id = selected_recipe_data['metadata'].get('id')
                        
                        # Registrar uso de la receta
                        #if meal_label not in used_recipe_ids:
                        #    used_recipe_ids[meal_label] = {}
                        #used_recipe_ids[meal_label][selected_recipe_id] = day
                        
                        # Crear MealDetailBase (sin daily_menu_id porque eso va en DailyMenuCreate)
                        meal_detail_data = MealDetailBase(
                            recipe_id=selected_recipe_id,
                            schedule=meal_idx + 1,
                            status=0,  # 0: pending
                            meal_type=MealTypeEnum(meal_label)  # Convertir string a Enum
                        )
                        
                        meal_details_for_day.append(meal_detail_data)
            
            # Crear DailyMenuCreate con todos los meal_details del día
            # Nota: plan_id se asignará automáticamente en el CRUD cuando se cree el plan
            daily_menu_data = DailyMenuCreate(
                plan_id=0,  # Este valor se ignorará/sobrescribirá en el CRUD
                day_of_week=day,
                meal_details=meal_details_for_day
            )
            
            daily_menus_data.append(daily_menu_data)
        
        # Crear el objeto PlanCreate con todos los daily_menus
        plan_create_data = PlanCreate(
            daily_menus=daily_menus_data
        )
        
        # Crear el plan usando el servicio que internamente usa el CRUD con cascada
        new_plan = PlanService.create_plan(db, plan_create_data, user_id)
        
        # Obtener plan completo con todos los detalles
        complete_plan = PlanService.get_current_plan(db, user_id)
        plan_response = PlanResponse.model_validate(complete_plan).model_dump()
    
        
        return {
            "result": f"✅ Plan semanal generado exitosamente.",
            "plan": plan_response,
            "summary": {
                "calories_daily": profile.calories_target,
                "protein_daily": profile.protein_target,
                "carbs_daily": profile.carbs_target,
                "fat_daily": profile.fat_target,
                "meals_per_day": profile.meals_per_day,
                "meal_distribution": meal_order,
                "calorie_distribution": meal_calorie_distribution,
                "calorie_ranges": calorie_ranges,
                "recipes_found": {meal: len(recipes) for meal, recipes in recipes_by_meal_type.items() if recipes},
                "total_recipes_used": sum(len(day.meal_details) for day in daily_menus_data)
            }
        }
        
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return {"result": f"Error generando plan: {str(e)}", "plan": None}
    finally:
        db.close()