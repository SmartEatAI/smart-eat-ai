from app.database import SessionLocal
from app.services.profile import ProfileService
from app.schemas.profile import ProfileResponse

from langchain.tools import tool

@tool
def get_user_profile_summary(user_id: int):
    """
    Obtiene un resumen del perfil del usuario incluyendo edad y metas.
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
        profile_data = ProfileResponse.model_validate(profile).model_dump()
        
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