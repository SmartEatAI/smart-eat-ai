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
    Ejecuta el reemplazo de una comida en el plan activo. Es el PASO 2 del flujo de cambio.
    
    PREREQUISITO OBLIGATORIO:
    SIEMPRE llamar suggest_recipe_alternatives ANTES para mostrar opciones al usuario.
    NUNCA llamar directamente sin que el usuario haya elegido una alternativa.
    
    CUÁNDO USAR:
    - DESPUÉS de que suggest_recipe_alternatives mostró alternativas
    - DESPUÉS de que el usuario eligió una opción (por nombre o número)
    
    CUÁNDO NO USAR:
    - Cuando el usuario dice "cambiar X" → primero usar suggest_recipe_alternatives
    - Sin confirmación del usuario sobre qué alternativa prefiere
    
    IDENTIFICAR LA COMIDA A REEMPLAZAR (una opción):
    - day_of_week + meal_type: "lunes" + "desayuno" (preferido)
    - meal_detail_id: ID del suggest_recipe_alternatives
    
    IDENTIFICAR LA NUEVA RECETA (una opción):
    - new_recipe_name: nombre de la receta elegida (preferido cuando el usuario dice el nombre)
    - new_recipe_id: ID numérico de alternatives_data
    
    EJEMPLOS:
    - Usuario dice "la opción 1 que es Kumara salad":
      → replace_meal_in_plan(user_id=X, day_of_week="lunes", meal_type="desayuno", new_recipe_name="Kumara salad")
    - Usuario dice "quiero la número 2":
      → identificar el nombre de la opción 2 y usar new_recipe_name
    
    Retorna: confirmación del cambio y plan actualizado.
    """
    db = SessionLocal()
    try:
        # Obtener usuario y validar
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"result": "Usuario no encontrado", "plan": None}
        
        # RESOLVER LA NUEVA RECETA
        new_recipe = None
        
        # Opción 1: Por recipe_id (ID del dataset)
        if new_recipe_id:
            new_recipe = db.query(Recipe).filter(Recipe.recipe_id == new_recipe_id).first()
            if not new_recipe:
                # Intentar también por id interno
                new_recipe = db.query(Recipe).filter(Recipe.id == new_recipe_id).first()
        
        # Opción 2: Por nombre de receta (búsqueda parcial case-insensitive)
        if not new_recipe and new_recipe_name:
            recipe_name_lower = new_recipe_name.lower().strip()
            # Buscar coincidencia exacta primero
            new_recipe = db.query(Recipe).filter(
                Recipe.name.ilike(recipe_name_lower)
            ).first()
            
            # Si no hay exacta, buscar parcial
            if not new_recipe:
                new_recipe = db.query(Recipe).filter(
                    Recipe.name.ilike(f"%{recipe_name_lower}%")
                ).first()
            
            if not new_recipe:
                return {
                    "result": f"No encontré una receta llamada '{new_recipe_name}'",
                    "plan": None
                }
        
        if not new_recipe:
            return {
                "result": "Debes proporcionar new_recipe_id O new_recipe_name para indicar la nueva receta",
                "plan": None
            }
        
        # Verificar restricciones dietéticas del usuario
        if user.profile and user.profile.diet_types:
            user_diets = {d.name.lower() for d in user.profile.diet_types}
            recipe_diets = {d.name.lower() for d in new_recipe.diet_types}
            
            # La receta debe incluir al menos una de las dietas del usuario
            if user_diets and not user_diets.intersection(recipe_diets):
                return {
                    "result": f"Esta receta no cumple con tus restricciones dietéticas ({', '.join(user_diets)})",
                    "plan": None
                }
        
        # RESOLVER EL MEAL_DETAIL_ID
        target_meal_detail_id = meal_detail_id
        
        # Si no se proporciona meal_detail_id, buscarlo por día y tipo de comida
        if not target_meal_detail_id and day_of_week and meal_type:
            # Normalizar día
            day_normalized = DAYS_MAP_ES.get(day_of_week.lower().strip())
            if not day_normalized:
                return {"result": f"Día '{day_of_week}' no reconocido", "plan": None}
            
            # Normalizar tipo de comida
            meal_type_normalized = MEAL_TYPE_MAP_ES.get(meal_type.lower().strip())
            if not meal_type_normalized:
                return {"result": f"Tipo de comida '{meal_type}' no reconocido", "plan": None}
            
            # Obtener plan activo
            plan = db.query(Plan).filter(
                Plan.user_id == user_id,
                Plan.active.is_(True)
            ).first()
            
            if not plan:
                return {"result": "No tienes un plan activo", "plan": None}
            
            # Buscar el meal_detail
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
                    "result": f"No encontré {meal_type} para el {day_of_week} en tu plan",
                    "plan": None
                }
        
        if not target_meal_detail_id:
            return {
                "result": "Debes proporcionar meal_detail_id O (day_of_week + meal_type) para identificar qué comida reemplazar",
                "plan": None
            }
        
        # Actualizar usando el servicio existente
        # Nota: update_meal_detail_recipe_id espera el recipe_id del dataset
        updated_meal = MealDetailService.update_meal_detail_recipe_id(
            db, 
            target_meal_detail_id, 
            new_recipe.recipe_id
        )
        
        if not updated_meal:
            return {"result": "No se pudo actualizar la comida", "plan": None}
        
        # Obtener plan actualizado
        current_plan = PlanService.get_current_plan(db, user_id)
        if current_plan:
            # mode='json' asegura que datetime se serialice como string ISO
            plan_response = PlanResponse.model_validate(current_plan).model_dump(mode='json')
            
            return {
                "result": f"✅ Comida reemplazada exitosamente por **{new_recipe.name}** ({new_recipe.calories} kcal, {new_recipe.protein}g proteína)",
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
                "result": f"✅ Comida reemplazada por {new_recipe.name}, pero no se encontró plan activo para mostrar",
                "plan": None
            }
            
    except Exception as e:
        db.rollback()
        logger.error(f"Error en replace_meal_in_plan: {str(e)}")
        return {"result": f"Error reemplazando comida: {str(e)}", "plan": None}
    finally:
        db.close()