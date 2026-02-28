from langchain.tools import tool
from app.services.recipe import RecipeService
from app.services.plan import PlanService
from app.schemas.plan import PlanResponse
from app.database import SessionLocal
from app.core.config_ollama import vector_db

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
            return {"result": f"No se encontraron recetas para '{query}'.", "recipes": []}
        resultado = f"Recetas encontradas para '{query}':\n"
        recipe_list = []
        for i, receta in enumerate(recetas, 1):
            resultado += f"{i}. {receta.name}\n"
            recipe_list.append({"id": receta.id, "name": receta.name})
        resultado += "¿Te gustaría ver los detalles de alguna receta en específico?"
        return {"result": resultado, "recipes": recipe_list}
    except Exception as e:
        return {"result": f"Error buscando recetas: {str(e)}", "recipes": []}
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
            return {"result": "Error: preference_type debe ser 'taste' o 'restriction'."}
        # Aquí se llamará a la lógica real para actualizar preferencias
        # Por simplicidad, solo devolvemos un string de éxito
        return {"result": f"Preferencia '{preference_type}' para '{item_name}' añadida al usuario {user_id}."}
    except Exception as e:
        return {"result": f"Error actualizando preferencias: {str(e)}"}
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
        plan = PlanService.get_current_plan(db, user_id)
        if not plan:
            return {"result": f"No se encontró el plan del usuario {user_id}.", "plan": None}
        plan_response = PlanResponse.model_validate(plan).dict()
        return {"result": "Plan encontrado", "plan": plan_response}
    except Exception as e:
        return {"result": f"Error recuperando el plan: {str(e)}", "plan": None}
    finally:
        db.close()

@tool
def buscar_en_base_datos(query: str):
    """Útil para buscar información específica sobre dietas, alimentos o nutrición."""
    docs = vector_db.similarity_search(query)
    return docs
    #return "Resultado de la búsqueda: [Aquí iría el contexto relevante]"

#nutrition_tools = [get_current_user_plan, search_recipes, update_user_preferences]
nutrition_tools = [buscar_en_base_datos]