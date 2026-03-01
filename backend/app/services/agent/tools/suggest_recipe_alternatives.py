from app.database import SessionLocal
from app.models.user import User
from app.core.recommender import swap_for_similar

from langchain.tools import tool


@tool
def suggest_recipe_alternatives(user_id: int, current_recipe_id: int, meal_label: str):
    """
    Sugiere recetas alternativas similares a la actual usando KNN.
    meal_label debe ser: 'breakfast', 'lunch', 'dinner', o 'snack'
    
    Devuelve hasta 3 alternativas con:
    - recipe_id: ID necesario para replace_meal_in_plan
    - name: Nombre de la receta
    - calories, protein, carbs, fat: Valores nutricionales
    """
    db = SessionLocal()
    try:
        # Obtener usuario
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"result": "Usuario no encontrado", "alternatives": []}
        
        # Obtener múltiples alternativas
        alternatives = []
        for _ in range(3):  # Intentar obtener 3 alternativas
            alternative = swap_for_similar(
                db=db,
                user=user,
                recipe_id=current_recipe_id,
                meal_label=meal_label,
                n_search=550
            )
            if alternative and alternative not in alternatives:
                alternatives.append(alternative)
        
        if not alternatives:
            return {
                "result": "No encontré alternativas similares que cumplan con tus restricciones",
                "alternatives": []
            }
        
        # Formatear respuesta con IDs claros
        formatted_alternatives = []
        for alt in alternatives:
            formatted_alternatives.append(
                f"[ID: {alt['recipe_id']}] {alt['name']} - {alt['calories']} kcal, {alt['protein']}g prot"
            )
        
        return {
            "result": f"Encontré {len(alternatives)} alternativas similares. Elige una diciéndome su ID:",
            "current_recipe_id": current_recipe_id,
            "alternatives": formatted_alternatives,
            "alternatives_data": alternatives,
            "reason": "basadas en similitud nutricional"
        }
        
    except Exception as e:
        return {"result": f"Error sugiriendo alternativas: {str(e)}", "alternatives": []}
    finally:
        db.close()
