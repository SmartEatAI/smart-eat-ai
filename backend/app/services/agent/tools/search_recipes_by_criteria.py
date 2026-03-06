from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from langchain.tools import tool
import logging
import time
import random  # <-- AÑADIDO: import random

from app.database import SessionLocal
from app.models.recipe import Recipe
from app.models.user import User
from app.models.plan import Plan
from app.core.config_ollama import llm


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
    Searches for recipes in the GENERAL DATABASE according to specific criteria. NOT related to the active plan.
    NEVER ask for clarification - use this tool immediately with whatever info provided.
    When user asks for recipes (ANY cuisine request), 
    call this tool right away with available parameters. If parameters missing, use defaults/null.
    Returns 5 recipes by default if not specified a number of recipes to return.

    Examples of when to use WITHOUT asking questions:
    - "show me low calorie recipes" → call with max_calories=null (tool handles it)
    - "find chicken recipes" → call with query="chicken"
    - "vegan breakfast ideas" → call with meal_type="breakfast", diet_type="vegan"

    Parameters: meal_type, diet_type, max_calories, min_protein, max_carbs, max_fat, query
    """
    db: Session = SessionLocal()
    start_time = time.time()
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return {"result": "User or profile not found", "recipes": []}

        profile = user.profile

        # ===== NUEVO: Valores por defecto para búsquedas implícitas =====
        if max_calories is None and query and "low calorie" in query.lower():
            max_calories = 500  # Default para "low calorie"
            logging.info(f"Implied max_calories set to: {max_calories}")

        if min_protein is None and query and "high protein" in query.lower():
            min_protein = 20  # Default para "high protein"
            logging.info(f"Implied min_protein set to: {min_protein}")

        # ===== OPTIMIZACIÓN 1: Filtros SQL básicos primero =====
        # Construimos la query base
        query_db = db.query(Recipe)
        
        # Aplicar filtros básicos de SQL (los más rápidos)
        if meal_type:
            query_db = query_db.join(Recipe.meal_types).filter(
                Recipe.meal_types.any(name=meal_type.lower())
            )
        
        # Filtros numéricos (muy rápidos en SQL)
        if max_calories is not None:
            query_db = query_db.filter(Recipe.calories <= max_calories)
        if min_protein is not None:
            query_db = query_db.filter(Recipe.protein >= min_protein)
        if max_carbs is not None:
            query_db = query_db.filter(Recipe.carbs <= max_carbs)
        if max_fat is not None:
            query_db = query_db.filter(Recipe.fat <= max_fat)
        
        # Excluir recetas del plan activo
        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user.id, Plan.active.is_(True))
            .first()
        )
        exclude_ids = set()
        if plan:
            exclude_ids = {
                meal.recipe_id 
                for day in plan.daily_menus 
                for meal in day.meal_details
            }
        
        # Obtener TODAS las recetas que pasan los filtros SQL
        # Pero limitamos a un número razonable para evitar sobrecarga
        all_recipes = query_db.limit(100).all()  # Limitamos a 100 recetas máximo
        logging.info(f"Total recipes after SQL filters: {len(all_recipes)}")

        # ===== OPTIMIZACIÓN 2: Filtrado por lotes sin paralelismo complejo =====
        # Determinamos si necesitamos el filtro LLM
        has_llm_filter = False
        restrictions_text = ""
        diet_text = ""
        
        if profile.restrictions or profile.diet_types:
            restriction_names = [r.name for r in profile.restrictions] if profile.restrictions else []
            restrictions_text = ", ".join(restriction_names)
            
            diet_type_names = [d.name for d in profile.diet_types] if profile.diet_types else []
            target_diets = {"vegan", "vegetarian"}
            diet_text_list = [name for name in diet_type_names if name.lower() in target_diets]
            diet_text = ", ".join(diet_text_list)
            
            if restriction_names or diet_text_list:
                has_llm_filter = True
                logging.info(f"LLM filter active - Restrictions: [{restrictions_text}], Diets: [{diet_text}]")

        # ===== OPTIMIZACIÓN 3: Procesamiento por lotes con early exit =====
        filtered_recipes = []
        recipes_processed = 0
        recipes_to_return = 5  # Número de recetas a devolver
        
        # Primero filtramos por diet_type si se proporcionó
        if diet_type:
            filtered_recipes = [
                r for r in all_recipes
                if diet_type.lower() in [d.name.lower() for d in r.diet_types]
            ]
        else:
            filtered_recipes = all_recipes.copy()
        
        # Filtramos por exclude_ids
        filtered_recipes = [r for r in filtered_recipes if r.recipe_id not in exclude_ids]
        
        # Si hay query de texto, aplicamos ese filtro ahora (es rápido)
        if query:
            query_lower = query.lower()
            filtered_recipes = [
                r for r in filtered_recipes
                if query_lower in r.name.lower() or 
                    (r.ingredients and query_lower in r.ingredients.lower())
            ]
        
        logging.info(f"Recipes after basic filters: {len(filtered_recipes)}")
        
        # ===== OPTIMIZACIÓN 4: LLM filter con early stopping =====
        if has_llm_filter and filtered_recipes:
            llm_valid_recipes = []
            
            for recipe in filtered_recipes:
                # Verificamos si ya tenemos suficientes recetas
                if len(llm_valid_recipes) >= recipes_to_return:
                    logging.info(f"Early stopping: found {recipes_to_return} valid recipes")
                    break
                
                recipes_processed += 1
                
                # Construir mensaje para LLM
                diet_line = f"and I require diets: [{diet_text}]." if diet_text else ""
                message = (
                    f"answer ONLY with YES or NO. "
                    f"I have a dietary profile with restrictions: [{restrictions_text}] {diet_line}"
                    f"Does this recipe comply with my restrictions: {recipe.name} Ingredients: [{recipe.ingredients}]"
                )
                
                try:
                    # Llamada al LLM
                    response = llm.invoke(message)
                    answer = response.content.strip().upper()
                    
                    logging.info(f"Recipe {recipes_processed}: {recipe.name} -> {answer}")
                    
                    if answer == "YES":
                        llm_valid_recipes.append(recipe)
                
                except Exception as e:
                    logging.warning(f"Error in LLM for recipe {recipe.name}: {e}")
                    continue
            
            # Reemplazamos filtered_recipes con las válidas
            filtered_recipes = llm_valid_recipes
            logging.info(f"Recipes after LLM filter: {len(filtered_recipes)} (processed {recipes_processed})")
        
        # ===== MODIFICADO: Preparar respuesta con randomización =====
        # Seleccionar aleatoriamente hasta 5 recetas
        if len(filtered_recipes) > 5:
            random.shuffle(filtered_recipes)
            selected_recipes = filtered_recipes[:5]
        else:
            selected_recipes = filtered_recipes

        response = [
            f"Name: {r.name}, protein: {r.protein}, carbs: {r.carbs}, fat: {r.fat}"
            for r in selected_recipes
        ]

        # ===== MODIFICADO: Si no hay resultados exactos, buscar alternativas cercanas con randomización =====
        if not response and (min_protein is not None or max_calories is not None):
            # Construir condiciones para búsqueda de alternativas
            close_conditions = []
            if max_calories is not None:
                close_conditions.append(Recipe.calories <= max_calories * 1.2)  # 20% más
            if min_protein is not None:
                close_conditions.append(Recipe.protein >= min_protein * 0.8)  # 20% menos
            
            # Buscar recetas alternativas
            close_query = db.query(Recipe)
            if close_conditions:
                close_query = close_query.filter(and_(*close_conditions))
            
            close_recipes = close_query.limit(30).all()
            
            # Excluir las del plan activo
            close_recipes = [r for r in close_recipes if r.recipe_id not in exclude_ids]
            
            # Seleccionar aleatoriamente hasta 5
            if len(close_recipes) > 5:
                random.shuffle(close_recipes)
                close_recipes = close_recipes[:5]
            
            close_response = [
                f"Name: {r.name}, protein: {r.protein}, carbs: {r.carbs}, fat: {r.fat}"
                for r in close_recipes
            ]
            
            if close_response:
                filter_type = "calories" if max_calories is not None else "protein"
                filter_value = max_calories if max_calories is not None else min_protein
                return {
                    "result": f"No exact matches for {filter_value}g of {filter_type}. Here are {len(close_response)} close alternatives:",
                    "recipes": close_response
                }

        elapsed_time = time.time() - start_time
        logging.info(f"Search completed in {elapsed_time:.2f} seconds")
        
        return {
            "result": f"Found {len(response)} recipes",
            "recipes": response
        }

    except Exception as e:
        logging.error(f"Error searching recipes: {str(e)}")
        db.rollback()
        return {"result": f"Error searching recipes: {str(e)}", "recipes": []}
    finally:
        db.close()