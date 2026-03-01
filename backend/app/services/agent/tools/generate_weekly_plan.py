from langchain.tools import tool
from app.services.recipe import RecipeService
from app.services.plan import PlanService
from app.schemas.plan import PlanResponse, PlanCreate
from app.database import SessionLocal
from app.utils.calculations import calculate_macros, calculate_fat_percentage, calculate_age
from app.core.recommender import get_meal_order
from app.models.user import User

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