from langchain.tools import tool
from app.services.recipe import RecipeService
from app.services.profile import ProfileService
from app.services.taste import TasteService
from fastapi import Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.database import SessionLocal

@tool
def search_recipes(query: str, meal_type_id: int = None):
    """
    Busca recetas en la base de datos por nombre o ingrediente. 
    Opcionalmente filtra por tipo de comida (desayuno, almuerzo, etc.).
    Úsala cuando el usuario quiera cambiar una comida o busque algo específico.
    """
    db = SessionLocal()
    try:
        recetas = RecipeService.get_recipes_by_meal_type(db, meal_type_id) if meal_type_id else []
        recetas = [r for r in recetas if query.lower() in r.name.lower() or query.lower() in (r.description or '')]
        if not recetas:
            return f"No se encontraron recetas para '{query}'."
        resultado = f"Recetas encontradas para '{query}':\n"
        for i, receta in enumerate(recetas, 1):
            resultado += f"{i}. {receta.name}\n"
        resultado += "¿Te gustaría ver los detalles de alguna receta en específico?"
        return resultado
    except Exception as e:
        return f"Error buscando recetas: {str(e)}"
    finally:
        db.close()

@tool
def update_user_preferences(user_id: int, preference_type: str, item_name: str):
    """
    Añade un nuevo gusto o restricción al perfil del usuario.
    preference_type debe ser 'taste' o 'restriction'.
    Úsala cuando el usuario diga cosas como 'No me gusta el tomate' o 'Soy alérgico a los frutos secos'.
    """
    db = SessionLocal()
    try:
        if preference_type not in ['taste', 'restriction']:
            return "Error: preference_type debe ser 'taste' o 'restriction'."
        # Aquí deberías llamar a la lógica real para actualizar preferencias
        # Por simplicidad, solo devolvemos un string de éxito
        return f"Preferencia '{preference_type}' para '{item_name}' añadida al usuario {user_id}."
    except Exception as e:
        return f"Error actualizando preferencias: {str(e)}"
    finally:
        db.close()

@tool
def get_current_user_plan(user_id: int):
    """
    Recupera el plan nutricional actual de los 7 días para el usuario.
    Úsala para saber qué está comiendo el usuario actualmente antes de sugerir cambios.
    """
    db = SessionLocal()
    try:
        perfil = ProfileService.get_user_profile(db, user_id=user_id)
        if not perfil:
            return f"No se encontró el perfil del usuario {user_id}."
        return perfil
    except Exception as e:
        return f"Error recuperando el plan: {str(e)}"
    finally:
        db.close()

nutrition_tools = [get_current_user_plan, search_recipes, update_user_preferences]