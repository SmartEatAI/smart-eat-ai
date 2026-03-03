from app.database import SessionLocal
from app.models.user import User
from app.models.taste import Taste
from app.models.restriction import Restriction
from app.crud.category import get_or_create_category

from langchain.tools import tool

@tool
def update_user_preference(user_id: int, preference_type: str, category_name: str):
    """
    Añade gustos, preferencias, restricciones, intolerancias o alergias al perfil del usuario.
    
    CUÁNDO USAR:
    - "No me gusta el pescado" → preference_type="restriction", category_name="pescado"
    - "Soy alérgico a los frutos secos" → preference_type="restriction", category_name="frutos secos"
    - "Me encanta el pollo" → preference_type="taste", category_name="pollo"
    - "Soy intolerante a la lactosa" → preference_type="restriction", category_name="lactosa"
    - "Prefiero comida mediterránea" → preference_type="taste", category_name="mediterránea"
    
    CUÁNDO NO USAR:
    - Para ver el perfil (usar get_user_profile_summary)
    - Para modificar el plan (usar suggest_recipe_alternatives + replace_meal_in_plan)
    
    PARÁMETROS:
    - preference_type: "taste" (gustos positivos) o "restriction" (alergias, intolerancias, rechazos)
    - category_name: el alimento, ingrediente o estilo culinario mencionado
    
    Esta información se usa automáticamente en futuras búsquedas y generación de planes.
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
