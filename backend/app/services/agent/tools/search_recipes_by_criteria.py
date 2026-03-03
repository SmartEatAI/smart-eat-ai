from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from langchain.tools import tool
import logging

from app.database import SessionLocal
from app.models.recipe import Recipe
from app.models.user import User
from app.models.plan import Plan
from app.core.config_ollama import vector_db


@tool
def search_recipes_by_criteria(
    user_id: int,
    meal_type: Optional[str] = None,
    diet_type: Optional[str] = None,
    max_calories: Optional[float] = None,
    min_protein: Optional[float] = None,
    max_carbs: Optional[float] = None,
    max_fat: Optional[float] = None,
    query: Optional[str] = None
):
    """
    Busca recetas en la BASE DE DATOS GENERAL según criterios específicos. NO está relacionada con el plan activo.
    
    CUÁNDO USAR (búsquedas generales de recetas):
    - "Busca recetas con pollo", "recetas veganas", "opciones bajas en calorías"
    - "Dame recetas altas en proteína", "recetas para el desayuno"
    - Cuando el usuario quiere EXPLORAR recetas nuevas SIN modificar su plan
    - Cuando pide recomendaciones generales o ideas de comidas
    
    CUÁNDO NO USAR (usa suggest_recipe_alternatives en su lugar):
    - "Quiero cambiar el desayuno del lunes" → suggest_recipe_alternatives
    - "Cambia la cena del domingo" → suggest_recipe_alternatives  
    - Cualquier solicitud de MODIFICAR una comida del plan activo
    
    DIFERENCIA CLAVE: Esta tool busca en toda la base de datos.
    suggest_recipe_alternatives busca alternativas SIMILARES a una comida específica del plan.
    
    Parámetros:
    - meal_type: breakfast, lunch, dinner, snack
    - diet_type: vegetarian, vegan, gluten-free, etc.
    - max_calories, min_protein, max_carbs, max_fat: filtros nutricionales
    - query: búsqueda semántica por ingredientes o descripción
    
    Por defecto devuelve 5 recetas.
    """
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return {"result": "Usuario o perfil no encontrado", "recipes": []}

        profile = user.profile

        required_diets = {
            d.name.lower() for d in profile.diet_types
        } if profile.diet_types else set()

        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user.id, Plan.active.is_(True))
            .first()
        )
        exclude_ids = (
            {
                meal.recipe_id 
                for day in plan.daily_menus 
                for meal in day.meal_details
            }
            if plan else set()
        )

        query_db = db.query(Recipe)
        if meal_type:
            query_db = query_db.join(Recipe.meal_types).filter(
                Recipe.meal_types.any(
                    name=meal_type.lower()
                )
            )
        if diet_type:
            query_db = query_db.join(Recipe.diet_types).filter(
                Recipe.diet_types.any(
                    name=diet_type.lower()
                )
            )
        recipes = query_db.all()
        logging.info(f"Total recetas tras filtro meal_type/diet_type: {len(recipes)}")

        # Filtrado nutricional y dietas
        filtered_recipes: List[Recipe] = []
        for recipe in recipes:
            if recipe.recipe_id in exclude_ids:
                continue
            recipe_diets = {d.name.lower() for d in recipe.diet_types}
            if required_diets and not required_diets.intersection(recipe_diets):
                continue
            if max_calories is not None and recipe.calories > max_calories:
                continue
            if min_protein is not None and recipe.protein < min_protein:
                continue
            if max_carbs is not None and recipe.carbs > max_carbs:
                continue
            if max_fat is not None and recipe.fat > max_fat:
                continue
            filtered_recipes.append(recipe)
        logging.info(f"Recetas tras filtro nutricional: {len(filtered_recipes)}")

        # Búsqueda semántica si hay query
        if query:
            vector_results = vector_db.similarity_search(query)
            vector_ids = {doc.metadata.get("recipe_id") for doc in vector_results}
            filtered_recipes = [r for r in filtered_recipes if r.recipe_id in vector_ids]
            logging.info(f"Recetas tras filtro semántico: {len(filtered_recipes)}")

        response = [
            f"Name: {r.name}, protein: {r.protein}, carbs: {r.carbs}, fat: {r.fat}"
            for r in filtered_recipes[:5]
        ]

        # Si no hay recetas exactas, muestra sugerencias cercanas
        if not response and min_protein is not None:
            close_recipes = [
                r for r in recipes
                if r.protein >= min_protein * 0.8 and r.recipe_id not in exclude_ids
            ]
            close_response = [
                f"Name: {r.name}, protein: {r.protein}, carbs: {r.carbs}, fat: {r.fat}"
                for r in close_recipes[:5]
            ]
            if close_response:
                return {
                    "result": f"No se encontraron recetas con al menos {min_protein}g de proteína exactos, pero aquí tienes opciones cercanas:",
                    "recipes": close_response
                }
            else:
                return {
                    "result": f"No se encontraron recetas con el criterio solicitado.",
                    "recipes": []
                }

        return {
            "result": f"Se encontraron {len(response)} recetas",
            "recipes": response
        }

    except Exception as e:
        logging.error(f"Error buscando recetas: {str(e)}")
        db.rollback()
        return {
            "result": f"Error buscando recetas: {str(e)}", 
            "recipes": []
        }
    finally:
        db.close()