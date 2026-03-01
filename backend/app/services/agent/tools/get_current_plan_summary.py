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
        
        # Convertir a diccionario serializable
        plan_data = PlanResponse.model_validate(current_plan).model_dump()
        
        return {
            "result": "Plan activo encontrado",
            "has_plan": True,
            "plan": plan_data,
        }
        
    except AttributeError as e:
        return {
            "result": f"Error al procesar el plan: {str(e)}",
            "has_plan": False,
            "plan": None
        }
    except Exception as e:
        return {
            "result": f"Error obteniendo plan: {str(e)}", 
            "has_plan": False, 
            "plan": None
        }
    finally:
        db.close()