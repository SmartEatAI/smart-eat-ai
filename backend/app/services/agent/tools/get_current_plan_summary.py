from app.database import SessionLocal
from app.services.plan import PlanService
from app.schemas.plan import PlanResponse

from langchain.tools import tool

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
        
        # Crear resumen legible usando el objeto directamente
        summary = _create_plan_summary(current_plan)
        
        print(summary)
        # También convertir a diccionario por si el agente necesita acceso estructurado
        plan_dict = PlanResponse.model_validate(current_plan).model_dump()
        
        # En algunos frameworks puedes adjuntar "artifacts" o "metadata"
        return {
            "message": summary,  # El agente usará esto
            "has_plan": True,
        }
        
    except Exception as e:
        return {
            "message": f"Error obteniendo plan: {str(e)}", 
            "has_plan": False
        }
    finally:
        db.close()


def _create_plan_summary(current_plan) -> str:
    """Crea un resumen legible del plan usando el objeto directamente"""
    
    # Mapeo de días (1 = Monday en el schema)
    DAYS_MAP = {
        1: "Lunes",
        2: "Martes", 
        3: "Miércoles",
        4: "Jueves",
        5: "Viernes",
        6: "Sábado",
        7: "Domingo"
    }
    
    # Mapeo de tipos de comida
    MEAL_TYPE_MAP = {
        "breakfast": "Desayuno",
        "lunch": "Almuerzo", 
        "dinner": "Cena",
        "snack": "Snack"
    }
    
    # Mapeo de horarios
    SCHEDULE_MAP = {
        1: "🌅 Desayuno (6:00-9:00)",
        2: "🌄 Media mañana (9:00-12:00)", 
        3: "☀️ Almuerzo (12:00-15:00)",
        4: "⛅ Media tarde (15:00-18:00)",
        5: "🌆 Cena (18:00-21:00)",
        6: "🌙 Noche (21:00+)"
    }
    
    daily_menus = current_plan.daily_menus
    
    if not daily_menus:
        return "Tu plan está activo pero no tiene menús diarios asignados."
    
    # Ordenar por día de la semana
    daily_menus.sort(key=lambda x: x.day_of_week)
    
    # Estadísticas generales
    total_meals = sum(len(menu.meal_details) for menu in daily_menus)
    active_plan = "✅ Activo" if current_plan.active else "❌ Inactivo"
    
    summary = f"📋 **Resumen de tu plan nutricional**\n\n"
    summary += f"📊 Estado: {active_plan}\n"
    summary += f"📅 Duración: {len(daily_menus)} días\n"
    summary += f"🍽️ Total comidas: {total_meals}\n"
    summary += f"🆔 ID del plan: {current_plan.id}\n\n"
    
    # Detalle por día
    summary += "**📅 Distribución semanal:**\n"
    
    # Acumuladores para estadísticas
    weekly_stats = {
        'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0,
        'meals_count': 0, 'days_with_meals': 0
    }
    
    for menu in daily_menus:
        day_num = menu.day_of_week
        day_name = DAYS_MAP.get(day_num, f"Día {day_num}")
        meals = menu.meal_details
        
        if meals:
            weekly_stats['days_with_meals'] += 1
        
        summary += f"\n📌 **{day_name}** (ID menú: {menu.id})\n"
        
        # Ordenar comidas por schedule
        meals.sort(key=lambda x: x.schedule)
        
        # Mostrar cada comida
        for meal in meals:
            recipe = meal.recipe
            
            # Estado de la comida
            status_icon = "✅" if meal.status == 1 else "⏳"
            
            # Tipo de comida
            meal_type_name = MEAL_TYPE_MAP.get(meal.meal_type, meal.meal_type.capitalize())
            
            # Información nutricional
            calories = recipe.calories
            protein = recipe.protein
            carbs = recipe.carbs
            fat = recipe.fat
            
            # Acumular estadísticas
            weekly_stats['calories'] += calories
            weekly_stats['protein'] += protein
            weekly_stats['carbs'] += carbs
            weekly_stats['fat'] += fat
            weekly_stats['meals_count'] += 1
            
            # Horario
            schedule_text = SCHEDULE_MAP.get(meal.schedule, f"Horario {meal.schedule}")
            
            # Información de la receta
            summary += f"  {status_icon} **{meal_type_name}**: {recipe.name}\n"
            summary += f"    • 📊 {calories} kcal | 🥩 {protein}g prot | 🍚 {carbs}g carb | 🥑 {fat}g grasa\n"
            summary += f"    • ⏰ {schedule_text}\n"
            
            # Mostrar categorías si existen
            if recipe.meal_types:
                meal_cats = [cat.name for cat in recipe.meal_types if cat.name]
                if meal_cats:
                    summary += f"    • 🍽️ Tipo: {', '.join(meal_cats)}\n"
            
            if recipe.diet_types:
                diet_cats = [cat.name for cat in recipe.diet_types if cat.name]
                if diet_cats:
                    summary += f"    • 🥗 Dieta: {', '.join(diet_cats)}\n"
            
            # Enlaces si existen
            if recipe.recipe_url or recipe.image_url:
                url = recipe.recipe_url or recipe.image_url
                summary += f"    • 🔗 [Ver receta]({url})\n"
        
        # Si no hay comidas para este día
        if not meals:
            summary += f"  📭 Sin comidas asignadas\n"
    
    return summary