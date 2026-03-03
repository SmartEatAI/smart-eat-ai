from app.database import SessionLocal
from app.services.profile import ProfileService
from app.schemas.profile import ProfileResponse

from langchain.tools import tool

@tool
def get_user_profile_summary(user_id: int):
    """
    Obtiene el perfil completo del usuario: datos personales, metas de salud, gustos y restricciones alimentarias.
    
    CUÁNDO USAR:
    - Cuando el usuario saluda o inicia conversación (para personalizar la respuesta)
    - Cuando pregunta por sus datos, perfil, preferencias o restricciones
    - Cuando dice: "mis datos", "mi perfil", "qué sabes de mí", "mis preferencias"
    
    CUÁNDO NO USAR:
    - Para ver el plan nutricional (usar get_current_plan_summary)
    - Para buscar recetas (usar search_recipes_by_criteria)
    
    Retorna: datos del perfil sin el nombre del usuario.
    """
    db = SessionLocal()
    try:
        profile = ProfileService.get_user_profile(db, user_id=user_id)
        
        if not profile:
            return {
                "result": "No se encontró un perfil para este usuario",
                "profile": None
            }
        
        # Convertir a diccionario para que sea serializable
        # mode='json' asegura que date/datetime se serialice como string ISO
        profile_data = ProfileResponse.model_validate(profile).model_dump(mode='json')
        
        return {
            "result": "Perfil encontrado",
            "profile": profile_data,
        }
        
    except Exception as e:
        return {
            "result": f"Error obteniendo perfil: {str(e)}",
            "profile": None
        }
    finally:
        db.close()