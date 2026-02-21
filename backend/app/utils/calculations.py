from typing import Dict, List, Union

def estimate_bodyfat(sex: str, category: str) -> float:
    """
    Estima el porcentaje de grasa corporal según tipo corporal.
    
    Args:
        sex (str): "Male" o "Female"
        category (str): "Lean", "Normal", "Stocky", "Obese"
    
    Returns:
        float: Porcentaje de grasa corporal
    """
    mapping = {
        "Male": {"Lean": 12, "Normal": 18, "Stocky": 25, "Obese": 32},
        "Female": {"Lean": 20, "Normal": 26, "Stocky": 33, "Obese": 40}
    }
    return mapping[sex][category]

def calculate_macros(sex: str, age: int, height: float, weight: float, 
                    bodyfat_pct: float, activity: str, goal: str) -> Dict[str, Union[int, float, List[str]]]:
    """
    Calcula los macros diarios según perfil del usuario.
    
    Args:
        sex (str): "Male" o "Female"
        age (int): Edad del usuario
        height (float): Altura en cm
        weight (float): Peso en kg
        bodyfat_pct (float): Porcentaje de grasa corporal
        activity (str): Nivel de actividad física
        goal (str): Objetivo del usuario
    
    Returns:
        Dict: Macros calculados y dietas recomendadas
    """
    # Calcular masa magra
    lean_mass = weight * (1 - bodyfat_pct / 100)
    
    # Metabolismo basal (BMR) según sexo
    if sex == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Factores de actividad física
    factors = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "High": 1.725,
        "Very High": 1.9
    }
    
    # Gasto energético diario total (TDEE)
    tdee = bmr * factors[activity]
    
    # Recomendaciones personalizadas según objetivo
    if goal == "Gain Muscle":
        calories = tdee * 1.1 + 150
        protein = lean_mass * 2.2
    elif goal == "Lose Weight":
        calories = tdee * 0.8
        protein = lean_mass * 2.2
    else:
        calories = tdee
        protein = lean_mass * 2.0
    
    fats = (calories * 0.25) / 9
    carbs = (calories - (protein * 4 + fats * 9)) / 4
    
    return {
        "calories": int(calories),
        "protein": int(protein),
        "fat": int(fats),
        "carbs": int(carbs),
    }