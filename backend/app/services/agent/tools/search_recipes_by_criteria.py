from typing import Optional
from app.database import SessionLocal
from app.models.user import User
from app.services.recipe import RecipeService
from app.core.config_ollama import vector_db

from langchain.tools import tool

@tool
def search_recipes_by_criteria(
    user_id: int,
    meal_type: Optional[str] = None,
    max_calories: Optional[float] = None,
    min_protein: Optional[float] = None,
    max_carbs: Optional[float] = None,
    max_fat: Optional[float] = None,
    query: Optional[str] = None
):
    """
    Busca recetas en la base de datos según criterios específicos.
    Úsala cuando necesites encontrar recetas que cumplan con ciertos macros.
    """
    db = SessionLocal()
    try:
        # Obtener perfil del usuario para conocer restricciones
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return {"result": "Usuario o perfil no encontrado", "recipes": []}
        
        profile = user.profile
        required_diets = {d.name.lower() for d in profile.diet_types}
        restrictions = {r.name.lower() for r in profile.restrictions}
        
        # Obtener todas las recetas
        recipes = RecipeService.get_all_recipes(db)
        
        filtered_recipes = []
        for recipe in recipes:
            # Verificar restricciones dietéticas
            recipe_diets = {d.name.lower() for d in recipe.diet_types}
            if not required_diets.issubset(recipe_diets):
                continue
            
            # Verificar restricciones por ingredientes
            recipe_ingredients = [ing.name.lower() for ing in recipe.ingredients]
            if any(restriction in ' '.join(recipe_ingredients) for restriction in restrictions):
                continue
            
            # Verificar tipo de comida
            if meal_type:
                recipe_meal_types = {m.name.lower() for m in recipe.meal_types}
                if meal_type.lower() not in recipe_meal_types:
                    continue
            
            # Calcular macros por porción
            calories_per_serving = recipe.calories / recipe.servings
            protein_per_serving = recipe.protein / recipe.servings
            carbs_per_serving = recipe.carbs / recipe.servings
            fat_per_serving = recipe.fat / recipe.servings
            
            # Aplicar filtros de macros
            if max_calories and calories_per_serving > max_calories:
                continue
            if min_protein and protein_per_serving < min_protein:
                continue
            if max_carbs and carbs_per_serving > max_carbs:
                continue
            if max_fat and fat_per_serving > max_fat:
                continue
            
            filtered_recipes.append(recipe)
        
        # Si hay query de texto, buscar en vector DB
        if query:
            docs = vector_db.similarity_search(query)
            recipe_ids_from_vector = []
            for doc in docs:
                if doc.metadata and 'recipe_id' in doc.metadata:
                    recipe_ids_from_vector.append(int(doc.metadata['recipe_id']))
            
            filtered_recipes = [r for r in filtered_recipes if r.id in recipe_ids_from_vector]
        
        # Formatear resultado
        recipe_list = []
        for recipe in filtered_recipes[:10]:
            recipe_list.append({
                "id": recipe.id,
                "name": recipe.name,
                "description": recipe.description,
                "meal_types": [m.name for m in recipe.meal_types],
                "calories_per_serving": round(recipe.calories / recipe.servings, 1),
                "protein_per_serving": round(recipe.protein / recipe.servings, 1),
                "carbs_per_serving": round(recipe.carbs / recipe.servings, 1),
                "fat_per_serving": round(recipe.fat / recipe.servings, 1),
                "prep_time": recipe.prep_time,
                "difficulty": recipe.difficulty
            })
        
        return {
            "result": f"Se encontraron {len(recipe_list)} recetas que cumplen los criterios",
            "recipes": recipe_list
        }
    except Exception as e:
        return {"result": f"Error buscando recetas: {str(e)}", "recipes": []}
    finally:
        db.close()
