from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from langchain.tools import tool

from app.database import SessionLocal
from app.models.recipe import Recipe
from app.models.user import User
from app.models.plan import Plan
from app.schemas.recipe import RecipeResponse
from app.core.config_ollama import vector_db


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
    Busca recetas según criterios nutricionales, tipo de comida
    y preferencias del perfil del usuario.
    """
    # print("Ejecutando basura \nsearch_recipes_by_criteria con criterios:")
    # print(f"User ID: {user_id}, Meal Type: {meal_type}, Max Calories: {max_calories}, Min Protein: {min_protein}, Max Carbs: {max_carbs}, Max Fat: {max_fat}, Query: {query}")
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

        recipes = query_db.all()

        filtered_recipes: List[Recipe] = []

        for recipe in recipes:

            if recipe.recipe_id in exclude_ids:
                continue

            recipe_diets = {d.name.lower() for d in recipe.diet_types}

            if required_diets and not required_diets.intersection(recipe_diets):
                continue

            calories = recipe.calories
            protein = recipe.protein
            carbs = recipe.carbs
            fat = recipe.fat

            if max_calories is not None and calories > max_calories:
                continue

            if min_protein is not None and protein < min_protein:
                continue

            if max_carbs is not None and carbs > max_carbs:
                continue

            if max_fat is not None and fat > max_fat:
                continue

            filtered_recipes.append(recipe)

        if query:
            docs = vector_db.similarity_search(query)
            recipe_ids = {
                int(doc.metadata["recipe_id"])
                for doc in docs
                if doc.metadata and "recipe_id" in doc.metadata
            }

            filtered_recipes = [r for r in filtered_recipes if r.recipe_id in recipe_ids
            ]

        response = [f"Name: {r.name}, protein: {r.protein}, carbs: {r.carbs}, fat: {r.fat}" for r in filtered_recipes[:5]]

        return {
            "result": f"Se encontraron {len(response)} recetas",
            "recipes": response
        }

    except Exception as e:
        return {
            "result": f"Error buscando recetas: {str(e)}",
            "recipes": []
        }

    finally:
        db.close()