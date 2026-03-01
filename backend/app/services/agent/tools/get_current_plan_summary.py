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
            return "No tienes un plan activo actualmente. ¿Te gustaría que genere uno?"
        
        # 1. Creamos el resumen formateado usando tu lógica actual
        summary = _create_plan_summary(current_plan)
        print(summary)
        # 2. DEVOLVEMOS SOLO EL STRING FORMATEADO
        return {
            "result": "Perfil encontrado",
            "plan": summary,
        }
        
    except Exception as e:
        return f"Error obteniendo plan: {str(e)}"
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
        1: "1",
        2: "2", 
        3: "3",
        4: "4",
        5: "5",
        6: "6"
    }
    
    daily_menus = current_plan.daily_menus
    
    if not daily_menus:
        return "Tu plan está activo pero no tiene menús diarios asignados."
    
    # Ordenar por día de la semana
    daily_menus.sort(key=lambda x: x.day_of_week)
    
    # Estadísticas generales
    total_meals = sum(len(menu.meal_details) for menu in daily_menus)
    active_plan = "Activo" if current_plan.active else "❌ Inactivo"
    
    summary = f"**Resumen de tu plan nutricional**\n\n"
    summary += f"Estado: {active_plan}\n"
    summary += f"Duración: {len(daily_menus)} días\n"
    summary += f"Total comidas: {total_meals}\n"
    summary += f"ID del plan: {current_plan.id}\n\n"
    
    # Detalle por día
    summary += "**Distribución semanal:**\n"
    
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
        
        summary += f"\n**{day_name}**\n"
        
        # Ordenar comidas por schedule
        meals.sort(key=lambda x: x.schedule)
        
        # Mostrar cada comida
        for meal in meals:
            recipe = meal.recipe
            
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
            schedule_text = SCHEDULE_MAP.get(f"Comida {meal.schedule}")
            
            # Información de la receta
            summary += f"{schedule_text}\n"
            summary += f"{recipe.name}\n"
            summary += f"- {calories} kcal {protein}g prot {carbs}g carb {fat}g grasa\n"
            
            # Enlaces si existen
            if recipe.recipe_url or recipe.image_url:
                url = recipe.recipe_url or recipe.image_url
                summary += f"[Ver receta]({url})\n"
        
        # Si no hay comidas para este día
        if not meals:
            summary += f"Sin comidas asignadas\n"
    
    return summary