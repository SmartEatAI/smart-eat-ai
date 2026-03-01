from app.database import SessionLocal
from app.services.plan import PlanService
from app.schemas.plan import PlanResponse
from app.models.user import User
from app.models.recipe import Recipe

from langchain.tools import tool


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