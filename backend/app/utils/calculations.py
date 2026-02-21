from datetime import date
from decimal import Decimal
from app.schemas.profile import ProfileBase, ProfileCreate

def calculate_age(birth_date: date) -> int:
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )

def calculate_macros(profile: ProfileCreate) -> ProfileCreate:
    """
    Calcula macros diarios según el modelo Profile.
    """
    age = calculate_age(profile.birth_date)
    
    # Masa magra
    lean_mass = profile.weight * Decimal(1 - profile.body_fat_percentage / 100)
    
    # BMR (Mifflin-St Jeor)
    if profile.gender.lower() == "male":
        bmr = 10 * profile.weight + Decimal("6.25") * profile.height - 5 * age + 5
    else:
        bmr = 10 * profile.weight + Decimal("6.25") * profile.height - 5 * age - 161
    
    # Factores alineados con tu Enum: low / medium / high
    activity_factors = {
        "low": Decimal("1.2"),
        "medium": Decimal("1.55"),
        "high": Decimal("1.725"),
    }
    
    tdee = bmr * activity_factors[profile.activity_level]
    
    # Objetivos alineados con tu Enum: lose_weight / maintain_weight / gain_weight
    if profile.goal == "gain_weight":
        calories = tdee * Decimal("1.1") + Decimal("150")
        protein = lean_mass * Decimal("2.2")
    elif profile.goal == "lose_weight":
        calories = tdee * Decimal("0.8")
        protein = lean_mass * Decimal("2.2")
    else:  # maintain_weight
        calories = tdee
        protein = lean_mass * Decimal("2.0")
    
    fats = (calories * Decimal("0.25")) / Decimal("9")
    carbs = (calories - (protein * Decimal("4") + fats * Decimal("9"))) / Decimal("4")
    
    profile.calories_target = calories
    profile.protein_target = protein
    profile.carbs_target = carbs
    profile.fat_target = fats
    
    return profile