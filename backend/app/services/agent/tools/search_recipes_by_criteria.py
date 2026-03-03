from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from langchain.tools import tool
import logging

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

        # Solo filtrar estrictamente por dietas veganas/vegetarianas (igual que en generate_weekly_plan)
        # Las demás dietas como "high protein" no deben excluir recetas
        target_strict_diets = {"vegan", "vegetarian"}
        required_diets = set()
        if profile.diet_types:
            for d in profile.diet_types:
                if d.name.lower() in target_strict_diets:
                    required_diets.add(d.name.lower())

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

        # Filtrado con IA para restricciones alimenticias
        use_llm_filter = False
        restrictions_text = ""
        diet_text = ""
        
        if profile.restrictions or profile.diet_types:
            # Obtener nombres de las restricciones del usuario
            restriction_names = [r.name for r in profile.restrictions] if profile.restrictions else []
            restrictions_text = ", ".join(restriction_names)
            
            # Verificar si hay dietas veganas/vegetarianas
            diet_type_names = [d.name for d in profile.diet_types] if profile.diet_types else []
            target_diets = {"vegan", "vegetarian"}
            diet_text_list = [name for name in diet_type_names if name.lower() in target_diets]
            diet_text = ", ".join(diet_text_list)
            
            # Activar filtro LLM si hay restricciones o dietas veganas/vegetarianas
            if restriction_names or diet_text_list:
                use_llm_filter = True
                logging.info(f"Aplicando filtro IA - Restricciones: [{restrictions_text}], Dietas: [{diet_text}]")
        
        if use_llm_filter:
            llm_filtered_recipes: List[Recipe] = []
            
            for recipe in filtered_recipes:
                # Construir mensaje para el LLM
                diet_line = f"y quiero dietas: [{diet_text}]." if diet_text else ""
                mensaje = (
                    f"responde SOLO con SI o NO. "
                    f"Tengo un perfil alimenticio con restriccion de [{restrictions_text}] {diet_line}"
                    f"Esta receta cumple con mis restricciones: {recipe.name} Ingredientes: [{recipe.ingredients}]"
                )
                
                try:
                    # Llamar al LLM para validar la receta
                    response = llm.invoke(mensaje)
                    respuesta = response.content.strip().upper()
                    
                    logging.info(f"Receta: {recipe.name} -> {respuesta}")
                    
                    # Si la respuesta es SI, añadir a filtradas
                    if respuesta == "SI":
                        llm_filtered_recipes.append(recipe)
                
                except Exception as e:
                    logging.warning(f"Error en LLM al evaluar receta {recipe.name}: {e}")
                    continue
            
            filtered_recipes = llm_filtered_recipes
            logging.info(f"Recetas tras filtro IA: {len(filtered_recipes)}")

        # Búsqueda por texto en nombre e ingredientes (búsqueda SQL normal)
        if query:
            query_lower = query.lower()
            filtered_recipes = [
                r for r in filtered_recipes 
                if query_lower in r.name.lower() or 
                    (r.ingredients and query_lower in r.ingredients.lower())
            ]
            logging.info(f"Recetas tras filtro por query '{query}': {len(filtered_recipes)}")

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