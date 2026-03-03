from app.database import SessionLocal
from app.models.user import User
from app.models.profile import Profile
from app.models.plan import Plan
from app.models.recipe import Recipe
from app.core.recommender import swap_for_similar
from app.core.config_ollama import llm
from typing import Optional
import logging

from langchain.tools import tool
from .constants import (
    DAYS_MAP as DAYS_MAP_ES,
    DAYS_NUM_TO_NAME,
    MEAL_TYPE_MAP as MEAL_TYPE_MAP_ES,
    MEAL_TYPE_TO_DISPLAY as MEAL_TYPE_TO_ES,
    get_meal_type_value as _get_meal_type_value
)

logger = logging.getLogger(__name__)


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
    Sugiere 3 recetas SIMILARES a una comida específica del PLAN ACTIVO del usuario.
    Es el PASO 1 para cambiar una comida del plan (el PASO 2 es replace_meal_in_plan).
    
    CUÁNDO USAR (modificar comidas del plan activo):
    - "Quiero cambiar el desayuno del lunes" → usar day_of_week + meal_type
    - "Cambia la cena del domingo" → usar day_of_week + meal_type
    - "No me gusta la receta X de mi plan" → usar recipe_name
    - "Busca alternativas para el almuerzo del martes" → usar day_of_week + meal_type
    
    CUÁNDO NO USAR (usa search_recipes_by_criteria en su lugar):
    - "Busca recetas veganas" → búsqueda general
    - "Dame recetas con pollo" → búsqueda por ingredientes
    - Cualquier búsqueda que NO sea para cambiar una comida específica del plan
    
    DIFERENCIA CLAVE: Esta tool busca alternativas SIMILARES a una comida del plan.
    search_recipes_by_criteria busca en toda la base de datos por criterios generales.
    
    FORMAS DE IDENTIFICAR LA COMIDA:
    - day_of_week + meal_type: "lunes" + "desayuno", "domingo" + "cena"
    - recipe_name: nombre de la receta que aparece en el plan
    
    FLUJO OBLIGATORIO:
    1. Llamar esta tool para obtener 3 alternativas
    2. Mostrar alternativas al usuario y preguntar cuál prefiere
    3. Cuando el usuario elija, llamar replace_meal_in_plan con la selección
    
    Días válidos: lunes, martes, miércoles, jueves, viernes, sábado, domingo
    Comidas válidas: desayuno, almuerzo/comida, cena, snack/merienda
    
    Retorna: alternativas con recipe_id y meal_detail_id para el reemplazo.
    """
    db = SessionLocal()
    try:
        # Obtener usuario
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"result": "Usuario no encontrado", "alternatives": []}
        
        # Obtener perfil para restricciones y dietas
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        use_llm_filter = False
        restrictions_text = ""
        diet_text = ""
        if profile:
            # Obtener nombres de las restricciones del usuario
            if profile.restrictions:
                restriction_names = [r.name for r in profile.restrictions]
                restrictions_text = ", ".join(restriction_names)
            else:
                restrictions_text = "ninguna"
            
            # Verificar si hay dietas veganas/vegetarianas (igual que en generate_weekly_plan)
            diet_type_names = [d.name for d in profile.diet_types] if profile.diet_types else []
            target_diets = {"vegan", "vegetarian"}
            diet_text_list = [name for name in diet_type_names if name.lower() in target_diets]
            diet_text = ", ".join(diet_text_list)
            
            # Activar filtro LLM solo si hay restricciones reales o dietas veganas/vegetarianas
            if (profile.restrictions and len(profile.restrictions) > 0) or diet_text_list:
                use_llm_filter = True
                logger.info(f"Filtro IA activado - Restricciones: [{restrictions_text}], Dietas: [{diet_text}]")
        
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
        
        # Obtener múltiples alternativas con validación LLM
        alternatives = []
        seen_ids = set()
        max_attempts = 20
        attempts = 0
        
        while len(alternatives) < 3 and attempts < max_attempts:
            attempts += 1
            candidate = swap_for_similar(
                db=db,
                user=user,
                recipe_id=actual_recipe_id,
                meal_label=meal_type_normalized,
                n_search=550
            )
            if not candidate:
                continue
            if candidate['recipe_id'] in seen_ids:
                continue
            
            # Si el usuario tiene restricciones/dietas, validar con LLM
            if use_llm_filter:
                # Obtener la receta completa para acceder a ingredientes
                recipe = db.query(Recipe).filter(Recipe.recipe_id == candidate['recipe_id']).first()
                if not recipe:
                    continue
                
                # Construir prompt igual que en generate_weekly_plan
                diet_line = f"y quiero dietas: [{diet_text}]." if diet_text else ""
                mensaje = (
                    f"responde SOLO con SI o NO. "
                    f"Tengo un perfil alimenticio con restriccion de [{restrictions_text}] {diet_line}."
                    f"Esta receta cumple con mis restricciones: {recipe.name} Ingredientes: [{recipe.ingredients}]"
                )
                try:
                    response = llm.invoke(mensaje)
                    respuesta = response.content.strip().upper()
                    if respuesta != "SI":
                        continue  # No cumple, probar siguiente candidato
                except Exception as e:
                    logger.warning(f"Error en LLM al evaluar receta {recipe.name}: {e}")
                    continue  # Ante error, saltamos esta receta
            
            # Si llegamos aquí, la receta es válida
            seen_ids.add(candidate['recipe_id'])
            alternatives.append(candidate)
        
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