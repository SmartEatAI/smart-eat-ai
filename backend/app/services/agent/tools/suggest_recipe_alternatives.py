from app.database import SessionLocal
from app.models.user import User
from app.core.recommender import swap_for_similar

from langchain.tools import tool


@tool
def suggest_recipe_alternatives(user_id: int, current_recipe_id: int, meal_label: str):
    """
    Sugiere recetas alternativas similares a la actual usando KNN.
    meal_label debe ser: 'breakfast', 'lunch', 'dinner', o 'snack'
    """
    db = SessionLocal()
    try:
        # Obtener usuario
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"result": "Usuario no encontrado", "alternatives": []}
        
        # Usar el recommender existente
        alternative = swap_for_similar(
            db=db,
            user=user,
            recipe_id=current_recipe_id,
            meal_label=meal_label,
            n_search=550
        )
        
        if not alternative:
            return {
                "result": "No encontré alternativas similares que cumplan con tus restricciones",
                "alternatives": []
            }
        
        # swap_for_similar devuelve una sola alternativa, pero podemos buscar más
        # Por ahora, devolvemos esa como principal
        return {
            "result": f"Encontré esta alternativa similar",
            "current_recipe_id": current_recipe_id,
            "alternatives": [alternative],
            "reason": "basada en similitud nutricional"
        }
        
    except Exception as e:
        return {"result": f"Error sugiriendo alternativas: {str(e)}", "alternatives": []}
    finally:
        db.close()
