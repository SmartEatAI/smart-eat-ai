from langchain.tools import tool
from app.database import SessionLocal
from typing import List, Dict, Any

# Servicios / Modelos / Esquemas
from app.services.profile import ProfileService

# Funciones
from app.core.recommender import get_meal_order

# Chroma / Embedding
from langchain_chroma import Chroma
from app.core.config_ollama import embeddings



def meal_calories_distribution(n_meals: int):
    """
    Funcion para calcular la distribucion de calorias según 
    la cantidad de comidas diarias.

    """
    mapping = {
        3: [0.3, 0.4, 0.3],
        4: [0.25, 0.3, 0.15, 0.3],
        5: [0.2, 0.1, 0.3, 0.1, 0.3],
        6: [0.2, 0.1, 0.25, 0.1, 0.25, 0.1]
    }
    return mapping.get(n_meals, mapping[3])

def calculate_calorie_ranges(calories_target: float, n_meals: int) -> Dict[str, Dict[str, float]]:
    """
    Calcula los rangos de calorías para cada tipo de comida
    """
    # Porcentajes máximos por tipo de comida
    calories_percents_max = {
        3: {"breakfast": 0.30, "lunch": 0.40, "dinner": 0.40},
        4: {"breakfast": 0.25, "lunch": 0.35, "snack": 0.10, "dinner": 0.35},
        5: {"breakfast": 0.25, "lunch": 0.35, "snack": 0.10, "dinner": 0.35},
        6: {"breakfast": 0.25, "lunch": 0.30, "snack": 0.10, "dinner": 0.30}
    }
    
    # Obtener la distribución para este número de comidas
    max_percents = calories_percents_max.get(n_meals, calories_percents_max[3])
    meal_order = get_meal_order(n_meals)
    
    # Crear diccionario con rangos por tipo de comida
    calorie_ranges = {}
    for i, meal_type in enumerate(meal_order):
        max_percent = max_percents[meal_type] if meal_type in max_percents else 0.35
        min_percent = max_percent / 2  # El mínimo es la mitad del máximo
        
        calorie_ranges[meal_type] = {
            "min": calories_target * min_percent,
            "max": calories_target * max_percent
        }
    
    return calorie_ranges


@tool
def all_recipes_for_user(user_id: int) -> List[Dict[str, Any]]:
    """
    Obtiene todas las recetas que coinciden con el perfil del usuario
    basado en tipos de comida, dietas y rangos de calorías.
    """
    db = SessionLocal()

    # Obtener perfil de usuario
    profile = ProfileService.get_user_profile(db, user_id)

    # Calcular rangos de calorías
    calorie_ranges = calculate_calorie_ranges(
        profile.calories_target, 
        profile.meals_per_day
    )

    # Filtro por tipo de comida sin repetir
    meal_types = list(dict.fromkeys(get_meal_order(profile.meals_per_day)))

    # Filtro por tipo de dieta
    diet_type_names = [diet_type.name for diet_type in profile.diet_types]

    vector_db = Chroma(
        persist_directory="ruta/a/tu/chroma_db",
        embedding_function=embeddings
    )

    # Resultados por tipo de comida
    all_recipes = {}

    for meal_type in meal_types:
            # Construir filtro de metadatos para este tipo de comida
            where_filter = {
                "$and": [
                    # Filtro por tipo de comida (exacto)
                    {"meal_types": {"$eq": meal_type}},
                    
                    # Filtro por tipo de dieta (el usuario puede tener múltiples)
                    {"diet_types": {"$in": diet_type_names}},
                    
                    # Filtro por rango de calorías
                    {
                        "$and": [
                            {"calories": {"$gte": calorie_ranges[meal_type]["min"]}},
                            {"calories": {"$lte": calorie_ranges[meal_type]["max"]}}
                        ]
                    }
                ]
            }

    
            # Búsqueda semántica con filtros
            results = vector_db.similarity_search(
                query=f"{meal_type}",
                k=10,  # Número de resultados por tipo de comida
                filter=where_filter
            )

            # Procesar resultados
            recipes_for_meal = []
            for doc in results:
                recipes_for_meal.append({
                    "name": doc.page_content.split("Name: ")[1].split(". Diet")[0] if "Name:" in doc.page_content else doc.page_content,
                    "metadata": doc.metadata,
                    "content": doc.page_content
                })
            
            all_recipes[meal_type] = recipes_for_meal
        
    return all_recipes