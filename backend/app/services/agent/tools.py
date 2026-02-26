from langchain.tools import tool
from app.services.recipe import RecipeService
from app.services.profile import ProfileService
from app.services.taste import TasteService

@tool
def search_recipes(query: str, meal_type_id: int = None):
    """
    Busca recetas en la base de datos por nombre o ingrediente. 
    Opcionalmente filtra por tipo de comida (desayuno, almuerzo, etc.).
    Úsala cuando el usuario quiera cambiar una comida o busque algo específico.
    """
    # Aquí invocas tu service o crud existente
    return #RecipeService.search_recipes(query=query, meal_type_id=meal_type_id)

@tool
def update_user_preferences(taste_name: str, preference_type: str):
    """
    Añade un nuevo gusto o restricción al perfil del usuario.
    preference_type debe ser 'taste' o 'restriction'.
    Úsala cuando el usuario diga cosas como 'No me gusta el tomate' o 'Soy alérgico a los frutos secos'.
    """
    # Aquí usas tus funciones de taste/restriction
    return #TasteService.add_to_profile(name=taste_name, type=preference_type)

@tool
def get_current_user_plan(user_id: int):
    """
    Recupera el plan nutricional actual de los 7 días para el usuario.
    Úsala para saber qué está comiendo el usuario actualmente antes de sugerir cambios.
    """
    return #ProfileService.get_current_plan(user_id=user_id)