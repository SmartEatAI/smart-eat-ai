from langchain.tools import tool
from app.services.recipe import RecipeService
from app.services.profile import ProfileService
from app.services.taste import TasteService
from fastapi import Depends
from app.database import get_db
from sqlalchemy.orm import Session

@tool
def search_recipes():
    """
    Busca recetas en la base de datos por nombre o ingrediente. 
    Opcionalmente filtra por tipo de comida (desayuno, almuerzo, etc.).
    Úsala cuando el usuario quiera cambiar una comida o busque algo específico.
    """
    # Aquí invocas tu service o crud existente
    return "Lista de recetas encontradas..."#RecipeService.search_recipes(query=query, meal_type_id=meal_type_id)

@tool
def update_user_preferences():
    """
    Añade un nuevo gusto o restricción al perfil del usuario.
    preference_type debe ser 'taste' o 'restriction'.
    Úsala cuando el usuario diga cosas como 'No me gusta el tomate' o 'Soy alérgico a los frutos secos'.
    """
    # Aquí usas tus funciones de taste/restriction
    return "Actualizacion realizada..."#TasteService.add_to_profile(name=taste_name, type=preference_type)

@tool
def get_current_user_plan():
    """
    Recupera el plan nutricional actual de los 7 días para el usuario.
    Úsala para saber qué está comiendo el usuario actualmente antes de sugerir cambios.
    """
    return "Este es el plan del usuario..."#ProfileService.get_user_profile(session=db, user_id=user_id)

nutrition_tools = [get_current_user_plan, search_recipes, update_user_preferences]