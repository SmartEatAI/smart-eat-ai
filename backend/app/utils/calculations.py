from typing import Dict
from datetime import date


def calculate_age(birth_date: date) -> int:
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def calculate_macros(
    gender: str,
    birth_date: date,
    height: float,
    weight: float,
    body_fat_percentage: float,
    activity_level: str,
    goal: str,
) -> Dict[str, int]:
    """
    Calcula macros diarios según el modelo Profile.
    """

    age = calculate_age(birth_date)

    # Masa magra
    lean_mass = weight * (1 - body_fat_percentage / 100)

    # BMR (Mifflin-St Jeor)
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Factores alineados con tu Enum: low / medium / high
    activity_factors = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.725,
    }

    tdee = bmr * activity_factors[activity_level]

    # Objetivos alineados con tu Enum: lose_weight / maintain_weight / gain_weight
    if goal == "gain_weight":
        calories = tdee * 1.1 + 150
        protein = lean_mass * 2.2
    elif goal == "lose_weight":
        calories = tdee * 0.8
        protein = lean_mass * 2.2
    else:  # maintain_weight
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