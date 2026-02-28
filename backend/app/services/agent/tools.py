from langchain.tools import tool
from app.services.recipe import RecipeService
from app.services.plan import PlanService
from app.services.profile import ProfileService
from app.services.meal_detail import MealDetailService
from app.schemas.plan import PlanResponse, PlanCreate
from app.schemas.recipe import RecipeResponse
from app.database import SessionLocal
from app.core.config_ollama import vector_db
from app.utils.calculations import calculate_macros, calculate_fat_percentage, calculate_age
from app.core.ml_model import ml_model
from app.core.recommender import swap_for_similar, get_meal_order
from app.models.user import User
from datetime import datetime, timedelta
from typing import Optional, List
import json
from app.models.recipe import Recipe
from app.crud.category import get_or_create_category

@tool
def buscar_en_base_datos(query: str):
    """Útil para buscar información específica sobre dietas, alimentos o nutrición."""
    docs = vector_db.similarity_search(query)
    return [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]

@tool
def search_recipes_by_criteria(
    user_id: int,
    meal_type: Optional[str] = None,
    max_calories: Optional[float] = None,
    min_protein: Optional[float] = None,
    max_carbs: Optional[float] = None,
    max_fat: Optional[float] = None,
    query: Optional[str] = None
):
    """
    Busca recetas en la base de datos según criterios específicos.
    Úsala cuando necesites encontrar recetas que cumplan con ciertos macros.
    """
    db = SessionLocal()
    try:
        # Obtener perfil del usuario para conocer restricciones
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return {"result": "Usuario o perfil no encontrado", "recipes": []}
        
        profile = user.profile
        required_diets = {d.name.lower() for d in profile.diet_types}
        restrictions = {r.name.lower() for r in profile.restrictions}
        
        # Obtener todas las recetas
        recipes = RecipeService.get_all_recipes(db)
        
        filtered_recipes = []
        for recipe in recipes:
            # Verificar restricciones dietéticas
            recipe_diets = {d.name.lower() for d in recipe.diet_types}
            if not required_diets.issubset(recipe_diets):
                continue
            
            # Verificar restricciones por ingredientes
            recipe_ingredients = [ing.name.lower() for ing in recipe.ingredients]
            if any(restriction in ' '.join(recipe_ingredients) for restriction in restrictions):
                continue
            
            # Verificar tipo de comida
            if meal_type:
                recipe_meal_types = {m.name.lower() for m in recipe.meal_types}
                if meal_type.lower() not in recipe_meal_types:
                    continue
            
            # Calcular macros por porción
            calories_per_serving = recipe.calories / recipe.servings
            protein_per_serving = recipe.protein / recipe.servings
            carbs_per_serving = recipe.carbs / recipe.servings
            fat_per_serving = recipe.fat / recipe.servings
            
            # Aplicar filtros de macros
            if max_calories and calories_per_serving > max_calories:
                continue
            if min_protein and protein_per_serving < min_protein:
                continue
            if max_carbs and carbs_per_serving > max_carbs:
                continue
            if max_fat and fat_per_serving > max_fat:
                continue
            
            filtered_recipes.append(recipe)
        
        # Si hay query de texto, buscar en vector DB
        if query:
            docs = vector_db.similarity_search(query)
            recipe_ids_from_vector = []
            for doc in docs:
                if doc.metadata and 'recipe_id' in doc.metadata:
                    recipe_ids_from_vector.append(int(doc.metadata['recipe_id']))
            
            filtered_recipes = [r for r in filtered_recipes if r.id in recipe_ids_from_vector]
        
        # Formatear resultado
        recipe_list = []
        for recipe in filtered_recipes[:10]:
            recipe_list.append({
                "id": recipe.id,
                "name": recipe.name,
                "description": recipe.description,
                "meal_types": [m.name for m in recipe.meal_types],
                "calories_per_serving": round(recipe.calories / recipe.servings, 1),
                "protein_per_serving": round(recipe.protein / recipe.servings, 1),
                "carbs_per_serving": round(recipe.carbs / recipe.servings, 1),
                "fat_per_serving": round(recipe.fat / recipe.servings, 1),
                "prep_time": recipe.prep_time,
                "difficulty": recipe.difficulty
            })
        
        return {
            "result": f"Se encontraron {len(recipe_list)} recetas que cumplen los criterios",
            "recipes": recipe_list
        }
    except Exception as e:
        return {"result": f"Error buscando recetas: {str(e)}", "recipes": []}
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
        # Obtener usuario y perfil
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return {"result": "No se encontró perfil para el usuario", "plan": None}
        
        profile = user.profile
        
        # Calcular macros si no están establecidos
        if not all([profile.calories_target, profile.protein_target, 
                   profile.carbs_target, profile.fat_target]):
            profile = calculate_macros(profile)
            db.commit()
        
        # Estimar body fat si no está establecido
        if not profile.body_fat_percentage:
            profile.body_fat_percentage = calculate_fat_percentage(profile)
            db.commit()
        
        # Obtener orden de comidas según meals_per_day
        meal_order = get_meal_order(profile.meals_per_day)
        
        # Obtener recetas disponibles (filtradas por dietas y restricciones)
        all_recipes = RecipeService.get_all_recipes(db)
        required_diets = {d.name.lower() for d in profile.diet_types}
        restrictions = {r.name.lower() for r in profile.restrictions}
        
        available_recipes = []
        for recipe in all_recipes:
            recipe_diets = {d.name.lower() for d in recipe.diet_types}
            if not required_diets.issubset(recipe_diets):
                continue
            
            recipe_ingredients = [ing.name.lower() for ing in recipe.ingredients]
            if any(restriction in ' '.join(recipe_ingredients) for restriction in restrictions):
                continue
            
            available_recipes.append(recipe)
        
        if not available_recipes:
            return {"result": "No hay recetas disponibles que cumplan con las restricciones", "plan": None}
        
        # Crear nuevo plan
        plan_data = PlanCreate(
            user_id=user_id,
            active=True,
            calories_target=profile.calories_target,
            protein_target=profile.protein_target,
            carbs_target=profile.carbs_target,
            fat_target=profile.fat_target
        )
        
        plan = PlanService.create_plan(db, plan_data)
        
        # Calcular calorías por comida (distribución típica)
        meal_calorie_distribution = {
            "breakfast": 0.25,
            "lunch": 0.35,
            "dinner": 0.3,
            "snack": 0.1
        }
        
        # Ajustar distribución según número de comidas
        if profile.meals_per_day == 3:
            # Sin snacks, redistribuir
            meal_calorie_distribution = {
                "breakfast": 0.3,
                "lunch": 0.4,
                "dinner": 0.3
            }
        elif profile.meals_per_day == 4:
            meal_calorie_distribution = {
                "breakfast": 0.25,
                "lunch": 0.3,
                "snack": 0.15,
                "dinner": 0.3
            }
        elif profile.meals_per_day == 5:
            meal_calorie_distribution = {
                "breakfast": 0.2,
                "snack": 0.1,
                "lunch": 0.3,
                "snack": 0.1,
                "dinner": 0.3
            }
        else:  # 6 comidas
            meal_calorie_distribution = {
                "breakfast": 0.2,
                "snack": 0.1,
                "lunch": 0.25,
                "snack": 0.1,
                "dinner": 0.25,
                "snack": 0.1
            }
        
        # Horarios por defecto (en minutos desde medianoche)
        meal_times = {
            "breakfast": 480,  # 8:00
            "snack": 600,       # 10:00 (primer snack)
            "lunch": 780,       # 13:00
            "snack": 960,       # 16:00 (segundo snack)
            "dinner": 1140,     # 19:00
            "snack": 1200       # 20:00 (snack nocturno)
        }
        
        # Generar menús diarios
        used_recipe_ids = set()  # Para evitar repetir recetas en el mismo plan
        
        for day in range(1, 8):  # 7 días
            daily_menu = PlanService.create_daily_menu(db, plan.id, day)
            
            # Para cada comida del día
            for meal_idx, meal_label in enumerate(meal_order):
                # Calcular calorías objetivo para esta comida
                meal_calorie_percent = meal_calorie_distribution.get(meal_label, 0.25)
                target_calories = profile.calories_target * meal_calorie_percent
                
                # Seleccionar receta para esta comida
                selected_recipe = None
                
                # Filtrar recetas por tipo de comida
                candidates = []
                for recipe in available_recipes:
                    if recipe.id in used_recipe_ids:
                        continue
                    
                    recipe_meal_types = {m.name.lower() for m in recipe.meal_types}
                    if meal_label not in recipe_meal_types:
                        continue
                    
                    # Verificar que los macros por porción no se excedan demasiado
                    calories_per_serving = recipe.calories / recipe.servings
                    if abs(calories_per_serving - target_calories) > target_calories * 0.3:
                        continue
                    
                    candidates.append(recipe)
                
                if candidates:
                    # Elegir el que más se acerque a las calorías objetivo
                    selected_recipe = min(candidates, 
                        key=lambda r: abs((r.calories / r.servings) - target_calories))
                    used_recipe_ids.add(selected_recipe.id)
                    
                    # Crear meal_detail
                    schedule_time = meal_times.get(meal_label, 480 + meal_idx * 120)
                    PlanService.create_meal_detail(
                        db,
                        daily_menu.id,
                        selected_recipe.id,
                        schedule_time,
                        meal_label.upper()
                    )
            
            # Resetear used_recipe_ids para el próximo día (permitir repeticiones entre días)
            used_recipe_ids = set()
        
        db.commit()
        
        # Obtener plan completo
        complete_plan = PlanService.get_plan_with_details(db, plan.id)
        plan_response = PlanResponse.model_validate(complete_plan).model_dump()
        
        # Calcular edad para el mensaje
        age = calculate_age(profile.birth_date)
        
        return {
            "result": f"✅ Plan semanal generado exitosamente para {age} años, {profile.goal}",
            "plan": plan_response,
            "summary": {
                "calories_daily": profile.calories_target,
                "protein_daily": profile.protein_target,
                "carbs_daily": profile.carbs_target,
                "fat_daily": profile.fat_target,
                "meals_per_day": profile.meals_per_day,
                "meal_distribution": meal_order
            }
        }
        
    except Exception as e:
        db.rollback()
        return {"result": f"Error generando plan: {str(e)}", "plan": None}
    finally:
        db.close()

@tool
def update_user_preference(user_id: int, preference_type: str, category_name: str):
    """
    Añade un nuevo gusto o restricción al perfil del usuario.
    preference_type: 'taste' (gusto) o 'restriction' (alergia/restricción)
    """
    db = SessionLocal()
    try:
        if preference_type not in ['taste', 'restriction']:
            return {"result": "Error: preference_type debe ser 'taste' o 'restriction'."}
        
        # Buscar o crear categoría
        category = get_or_create_category(db, category_name)
        
        # Añadir al perfil
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return {"result": "Usuario o perfil no encontrado", "profile": None}
        
        profile = user.profile
        
        if preference_type == 'taste':
            if category not in profile.tastes:
                profile.tastes.append(category)
            result_msg = f"👍 Gusto '{category_name}' añadido a tu perfil"
        else:
            if category not in profile.restrictions:
                profile.restrictions.append(category)
            result_msg = f"⚠️ Restricción '{category_name}' añadida a tu perfil"
        
        db.commit()
        
        # Recalcular macros si es necesario (por si la restricción afecta)
        if preference_type == 'restriction':
            # Podrías querer regenerar el plan si hay un plan activo
            pass
        
        from app.schemas.profile import ProfileResponse
        profile_response = ProfileResponse.model_validate(profile).model_dump()
        
        return {
            "result": result_msg,
            "profile": profile_response
        }
    except Exception as e:
        db.rollback()
        return {"result": f"Error actualizando preferencias: {str(e)}", "profile": None}
    finally:
        db.close()

@tool
def suggest_recipe_alternatives(user_id: int, current_recipe_id: int, meal_label: str):
    """
    Sugiere recetas alternativas similares a la actual usando KNN.
    meal_label debe ser: 'breakfast', 'lunch', 'dinner', o 'snack'
    """
    db = SessionLocal()
    try:
        # Obtener usuario
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"result": "Usuario no encontrado", "alternatives": []}
        
        # Usar el recommender existente
        alternative = swap_for_similar(
            db=db,
            user=user,
            recipe_id=current_recipe_id,
            meal_label=meal_label,
            n_search=550
        )
        
        if not alternative:
            return {
                "result": "No encontré alternativas similares que cumplan con tus restricciones",
                "alternatives": []
            }
        
        # swap_for_similar devuelve una sola alternativa, pero podemos buscar más
        # Por ahora, devolvemos esa como principal
        return {
            "result": f"Encontré esta alternativa similar",
            "current_recipe_id": current_recipe_id,
            "alternatives": [alternative],
            "reason": "basada en similitud nutricional"
        }
        
    except Exception as e:
        return {"result": f"Error sugiriendo alternativas: {str(e)}", "alternatives": []}
    finally:
        db.close()

@tool
def replace_meal_in_plan(user_id: int, daily_menu_id: int, meal_detail_id: int, new_recipe_id: int):
    """
    Reemplaza una comida específica en el plan actual con una nueva receta.
    """
    db = SessionLocal()
    try:
        from app.services.meal_detail import MealDetailService
        
        # Verificar que la receta existe y cumple restricciones
        user = db.query(User).filter(User.id == user_id).first()
        new_recipe = db.query(Recipe).filter(Recipe.id == new_recipe_id).first()
        
        if not new_recipe:
            return {"result": "La receta seleccionada no existe", "plan": None}
        
        # Verificar restricciones del usuario
        if user and user.profile:
            required_diets = {d.name.lower() for d in user.profile.diet_types}
            recipe_diets = {d.name.lower() for d in new_recipe.diet_types}
            
            if not required_diets.issubset(recipe_diets):
                return {"result": "Esta receta no cumple con tus restricciones dietéticas", "plan": None}
        
        # Actualizar meal_detail
        updated_meal = MealDetailService.update_meal_detail(
            db, 
            meal_detail_id, 
            {"recipe_id": new_recipe_id}
        )
        
        if not updated_meal:
            return {"result": "No se pudo actualizar la comida", "plan": None}
        
        db.commit()
        
        # Obtener plan actualizado
        current_plan = PlanService.get_current_plan(db, user_id)
        if current_plan:
            plan_response = PlanResponse.model_validate(current_plan).model_dump()
            
            # Obtener nombre de la nueva receta para el mensaje
            recipe_name = new_recipe.name
            
            return {
                "result": f"✅ Comida reemplazada exitosamente por '{recipe_name}'",
                "plan": plan_response
            }
        else:
            return {"result": "Comida reemplazada pero no se encontró plan activo", "plan": None}
            
    except Exception as e:
        db.rollback()
        return {"result": f"Error reemplazando comida: {str(e)}", "plan": None}
    finally:
        db.close()

@tool
def get_user_profile_summary(user_id: int):
    """
    Obtiene un resumen del perfil del usuario incluyendo edad y metas.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return {"result": "Perfil no encontrado", "profile": None}
        
        profile = user.profile
        age = calculate_age(profile.birth_date)
        
        # Calcular % grasa si no está
        if not profile.body_fat_percentage:
            profile.body_fat_percentage = calculate_fat_percentage(profile)
        
        from app.schemas.profile import ProfileResponse
        profile_data = ProfileResponse.model_validate(profile).model_dump()
        
        summary = {
            "edad": age,
            "género": profile.gender,
            "peso": f"{profile.weight} kg",
            "altura": f"{profile.height} cm",
            "objetivo": profile.goal,
            "comidas_diarias": profile.meals_per_day,
            "calorías_diarias": profile.calories_target or "Por calcular",
            "proteína_diaria": profile.protein_target or "Por calcular",
            "gustos": [t.name for t in profile.tastes],
            "restricciones": [r.name for r in profile.restrictions],
            "tipo_dieta": [d.name for d in profile.diet_types]
        }
        
        return {
            "result": "Perfil encontrado",
            "profile": profile_data,
            "summary": summary
        }
    except Exception as e:
        return {"result": f"Error obteniendo perfil: {str(e)}", "profile": None}
    finally:
        db.close()

@tool
def get_current_plan_summary(user_id: int):
    """
    Obtiene un resumen del plan activo del usuario.
    """
    db = SessionLocal()
    try:
        current_plan = PlanService.get_current_plan(db, user_id)
        
        if not current_plan:
            return {
                "result": "No tienes un plan activo actualmente. ¿Te gustaría que genere uno?",
                "has_plan": False,
                "plan": None
            }
        
        plan_response = PlanResponse.model_validate(current_plan).model_dump()
        
        # Crear resumen por días
        daily_summary = []
        for daily_menu in current_plan.daily_menus:
            day_meals = []
            total_calories_day = 0
            
            for meal in daily_menu.meal_details:
                recipe = meal.recipe
                calories_per_serving = recipe.calories / recipe.servings
                total_calories_day += calories_per_serving
                
                day_meals.append({
                    "tipo": meal.meal_type,
                    "receta": recipe.name,
                    "calorías": round(calories_per_serving, 1),
                    "proteína": round(recipe.protein / recipe.servings, 1),
                    "horario": f"{meal.schedule // 60}:{meal.schedule % 60:02d}"
                })
            
            daily_summary.append({
                "día": daily_menu.day_of_week,
                "comidas": day_meals,
                "total_calorías_día": round(total_calories_day, 1)
            })
        
        return {
            "result": "Plan activo encontrado",
            "has_plan": True,
            "plan": plan_response,
            "summary": {
                "calorías_diarias_objetivo": current_plan.calories_target,
                "días": daily_summary
            }
        }
        
    except Exception as e:
        return {"result": f"Error obteniendo plan: {str(e)}", "has_plan": False, "plan": None}
    finally:
        db.close()

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