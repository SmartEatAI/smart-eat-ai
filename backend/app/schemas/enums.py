from enum import Enum

# Definicion de Enums para que Pydantic valide los strings permitidos
class GoalEnum(str, Enum):
    lose_weight = "lose_weight"
    maintain_weight = "maintain_weight"
    gain_weight = "gain_weight"

class ActivityLevelEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class DietTypeEnum(str, Enum):
    high_protein = "high_protein"
    low_carb = "low_carb"
    vegan = "vegan"
    vegetarian = "vegetarian"
    low_calorie = "low_calorie"
    high_fiber = "high_fiber"
    high_carb = "high_carb"

class BodyTypeEnum(str, Enum):
    lean = "lean"
    normal = "normal"
    stocky = "stocky"
    obese = "obese"

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    
class MealTypeEnum(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"

class MessageRoleEnum(str, Enum):
    chef = "chef"
    user = "user"