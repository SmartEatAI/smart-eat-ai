from app.database import SessionLocal
from app.models.user import User
from app.models.taste import Taste
from app.models.restriction import Restriction
from app.crud.category import get_or_create_category

from langchain.tools import tool

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
        
        # Buscar o crear categoría con el modelo correcto
        model = Taste if preference_type == 'taste' else Restriction
        category = get_or_create_category(db, model, category_name)
        
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
        # mode='json' asegura que date/datetime se serialice como string ISO
        profile_response = ProfileResponse.model_validate(profile).model_dump(mode='json')
        
        return {
            "result": result_msg,
            "profile": profile_response
        }
    except Exception as e:
        db.rollback()
        return {"result": f"Error actualizando preferencias: {str(e)}", "profile": None}
    finally:
        db.close()
