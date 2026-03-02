from app.database import SessionLocal
from app.models.user import User
from app.models.plan import Plan
from app.models.recipe import Recipe
from app.core.recommender import swap_for_similar
from typing import Optional
import logging

from langchain.tools import tool

logger = logging.getLogger(__name__)

# Mapeo de días en español a números
DAYS_MAP_ES = {
    "lunes": 1, "martes": 2, "miércoles": 3, "miercoles": 3,
    "jueves": 4, "viernes": 5, "sábado": 6, "sabado": 6, "domingo": 7,
    "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4,
    "friday": 5, "saturday": 6, "sunday": 7
}

# Mapeo inverso de números a nombres de días
DAYS_NUM_TO_NAME = {
    1: "lunes", 2: "martes", 3: "miércoles", 4: "jueves",
    5: "viernes", 6: "sábado", 7: "domingo"
}

# Mapeo de tipos de comida en español
MEAL_TYPE_MAP_ES = {
    "desayuno": "breakfast", "almuerzo": "lunch", "comida": "lunch",
    "cena": "dinner", "snack": "snack", "merienda": "snack",
    "breakfast": "breakfast", "lunch": "lunch", "dinner": "dinner"
}

# Mapeo inverso de meal_type a español
MEAL_TYPE_TO_ES = {
    "breakfast": "desayuno", "lunch": "almuerzo", 
    "dinner": "cena", "snack": "snack"
}


def _get_meal_type_value(meal_type) -> str:
    """Extrae el valor string del meal_type, sea enum o string."""
    if hasattr(meal_type, 'value'):
        return meal_type.value.lower()
    return str(meal_type).lower()


def _find_meal_by_recipe_name(plan, recipe_name: str):
    """
    Busca una comida en el plan por nombre de receta (búsqueda parcial case-insensitive).
    Retorna (daily_menu, meal_detail) o (None, None) si no encuentra.
    """
    recipe_name_lower = recipe_name.lower().strip()
    
    for dm in plan.daily_menus:
        for md in dm.meal_details:
            if md.recipe and recipe_name_lower in md.recipe.name.lower():
                return dm, md
    return None, None


def _find_meal_by_day_and_type(plan, day_num: int, meal_type_normalized: str):
    """
    Busca una comida específica por día y tipo de comida.
    Retorna (daily_menu, meal_detail) o (None, None) si no encuentra.
    """
    for dm in plan.daily_menus:
        if dm.day_of_week == day_num:
            for md in dm.meal_details:
                md_meal_type = _get_meal_type_value(md.meal_type)
                if md_meal_type == meal_type_normalized:
                    return dm, md
    return None, None


@tool
def suggest_recipe_alternatives(
    user_id: int, 
    day_of_week: Optional[str] = None, 
    meal_type: Optional[str] = None,
    recipe_name: Optional[str] = None,
    current_recipe_id: Optional[int] = None
):
    """
    Sugiere recetas alternativas similares a una comida actual del plan.
    
    Puedes identificar la comida de TRES formas:
    1. Por día y tipo: day_of_week="domingo", meal_type="desayuno"
    2. Por nombre de receta: recipe_name="abbys pecan apple cake"
    3. Por ID de receta: current_recipe_id=12345 (menos común)
    
    Parámetros:
    - user_id: ID del usuario (obligatorio)
    - day_of_week: Día de la semana (ej: "lunes", "domingo") - usar con meal_type
    - meal_type: Tipo de comida (ej: "desayuno", "cena", "snack") - usar con day_of_week  
    - recipe_name: Nombre de la receta a cambiar (búsqueda parcial)
    - current_recipe_id: ID de la receta actual (opcional, se detecta automáticamente)
    
    Devuelve alternativas con recipe_id para usar en replace_meal_in_plan.
    """
    db = SessionLocal()
    try:
        # Obtener usuario
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"result": "Usuario no encontrado", "alternatives": []}
        
        # Obtener plan activo
        plan = db.query(Plan).filter(
            Plan.user_id == user_id, 
            Plan.active.is_(True)
        ).first()
        
        if not plan:
            return {"result": "No tienes un plan activo. Genera uno primero.", "alternatives": []}
        
        daily_menu = None
        meal_detail = None
        day_name_es = ""
        meal_type_es = ""
        meal_type_normalized = None
        
        # OPCIÓN 1: Buscar por nombre de receta
        if recipe_name:
            daily_menu, meal_detail = _find_meal_by_recipe_name(plan, recipe_name)
            if meal_detail:
                day_name_es = DAYS_NUM_TO_NAME.get(daily_menu.day_of_week, f"día {daily_menu.day_of_week}")
                meal_type_normalized = _get_meal_type_value(meal_detail.meal_type)
                meal_type_es = MEAL_TYPE_TO_ES.get(meal_type_normalized, meal_type_normalized)
                logger.info(f"Encontré '{recipe_name}' en {day_name_es} - {meal_type_es}")
            else:
                # Listar las recetas disponibles en el plan para ayudar al usuario
                available_recipes = []
                for dm in plan.daily_menus:
                    for md in dm.meal_details:
                        if md.recipe:
                            available_recipes.append(md.recipe.name)
                
                return {
                    "result": f"No encontré '{recipe_name}' en tu plan. Recetas disponibles: {', '.join(available_recipes[:10])}...",
                    "alternatives": []
                }
        
        # OPCIÓN 2: Buscar por día y tipo de comida
        elif day_of_week and meal_type:
            # Normalizar día de la semana
            day_normalized = DAYS_MAP_ES.get(day_of_week.lower().strip())
            if not day_normalized:
                return {
                    "result": f"Día '{day_of_week}' no reconocido. Usa: lunes, martes, miércoles, jueves, viernes, sábado, domingo",
                    "alternatives": []
                }
            
            # Normalizar tipo de comida
            meal_type_normalized = MEAL_TYPE_MAP_ES.get(meal_type.lower().strip())
            if not meal_type_normalized:
                return {
                    "result": f"Tipo de comida '{meal_type}' no reconocido. Usa: desayuno, almuerzo/comida, cena, snack",
                    "alternatives": []
                }
            
            daily_menu, meal_detail = _find_meal_by_day_and_type(plan, day_normalized, meal_type_normalized)
            day_name_es = day_of_week.lower()
            meal_type_es = meal_type.lower()
            
            if not meal_detail:
                # Debug: mostrar qué comidas hay ese día
                available_meals = []
                for dm in plan.daily_menus:
                    if dm.day_of_week == day_normalized:
                        for md in dm.meal_details:
                            mt = _get_meal_type_value(md.meal_type)
                            available_meals.append(f"{MEAL_TYPE_TO_ES.get(mt, mt)}: {md.recipe.name if md.recipe else 'sin receta'}")
                
                if available_meals:
                    return {
                        "result": f"No encontré '{meal_type}' para el {day_of_week}. Comidas disponibles ese día:\n" + "\n".join(available_meals),
                        "alternatives": []
                    }
                else:
                    return {
                        "result": f"No hay comidas programadas para el {day_of_week} en tu plan",
                        "alternatives": []
                    }
        else:
            return {
                "result": "Debes especificar: (day_of_week + meal_type) O (recipe_name) para identificar la comida a cambiar",
                "alternatives": []
            }
        
        if not meal_detail:
            return {
                "result": "No se pudo identificar la comida a cambiar",
                "alternatives": []
            }
        
        # Obtener el recipe_id actual (del dataset, no el id interno)
        current_recipe = meal_detail.recipe
        if not current_recipe:
            return {"result": "La comida no tiene una receta asociada", "alternatives": []}
            
        actual_recipe_id = current_recipe_id or current_recipe.recipe_id
        
        # Si no tenemos meal_type_normalized, obtenerlo del meal_detail
        if not meal_type_normalized:
            meal_type_normalized = _get_meal_type_value(meal_detail.meal_type)
        
        # Obtener múltiples alternativas
        alternatives = []
        seen_ids = set()
        for _ in range(8):  # Intentar más veces para obtener 3 únicas
            alternative = swap_for_similar(
                db=db,
                user=user,
                recipe_id=actual_recipe_id,
                meal_label=meal_type_normalized,
                n_search=550
            )
            if alternative and alternative['recipe_id'] not in seen_ids:
                seen_ids.add(alternative['recipe_id'])
                alternatives.append(alternative)
                if len(alternatives) >= 3:
                    break
        
        if not alternatives:
            return {
                "result": f"No encontré alternativas similares a '{current_recipe.name}' que cumplan con tus restricciones dietéticas",
                "alternatives": [],
                "meal_detail_id": meal_detail.id,
                "daily_menu_id": daily_menu.id
            }
        
        # Formatear respuesta con IDs claros
        formatted_alternatives = []
        for i, alt in enumerate(alternatives, 1):
            formatted_alternatives.append(
                f"{i}. **{alt['name']}** (ID: {alt['recipe_id']}) - {alt['calories']} kcal, {alt['protein']}g proteína, {alt['carbs']}g carbs"
            )
        
        # Información de la comida actual
        current_meal_info = f"**Comida actual** ({meal_type_es} del {day_name_es}): {current_recipe.name} ({current_recipe.calories} kcal)"
        
        return {
            "result": f"{current_meal_info}\n\n**Alternativas disponibles:**\n" + "\n".join(formatted_alternatives),
            "meal_detail_id": meal_detail.id,
            "daily_menu_id": daily_menu.id,
            "current_recipe_id": actual_recipe_id,
            "current_recipe_name": current_recipe.name,
            "day_of_week": day_name_es,
            "meal_type": meal_type_es,
            "alternatives_data": alternatives,
            "instruction": "Pregunta al usuario cuál alternativa prefiere (por número o nombre) y usa replace_meal_in_plan con el meal_detail_id y new_recipe_id correspondiente"
        }
        
    except Exception as e:
        logger.error(f"Error en suggest_recipe_alternatives: {str(e)}")
        return {"result": f"Error sugiriendo alternativas: {str(e)}", "alternatives": []}
    finally:
        db.close()
