"""
Shared constants for the nutritional agent tools.
Centralizes mappings for days, meal types, and other configurations.
"""

# Mapping of days in Spanish/English to numbers (ISO weekday: Monday=1)
DAYS_MAP = {
    # Spanish
    "lunes": 1, "martes": 2, "miércoles": 3, "miercoles": 3,
    "jueves": 4, "viernes": 5, "sábado": 6, "sabado": 6, "domingo": 7,
    # English
    "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4,
    "friday": 5, "saturday": 6, "sunday": 7
}

# Reverse mapping: number to day name (Spanish)
DAYS_NUM_TO_NAME = {
    1: "lunes", 2: "martes", 3: "miércoles", 4: "jueves",
    5: "viernes", 6: "sábado", 7: "domingo"
}

# Mapping of meal types from Spanish to English (internal)
MEAL_TYPE_MAP = {
    # Spanish
    "desayuno": "breakfast", 
    "almuerzo": "lunch", 
    "comida": "lunch",
    "cena": "dinner", 
    "snack": "snack", 
    "merienda": "snack",
    # English (for normalization)
    "breakfast": "breakfast", 
    "lunch": "lunch", 
    "dinner": "dinner"
}

# Reverse mapping: English to Spanish (for displaying to the user)
MEAL_TYPE_TO_DISPLAY = {
    "breakfast": "desayuno", 
    "lunch": "almuerzo", 
    "dinner": "cena", 
    "snack": "snack"
}


def normalize_day(day_input: str) -> int | None:
    """
    Normalizes a day of the week to its corresponding number.
    Returns None if not recognized.
    """
    if not day_input:
        return None
    return DAYS_MAP.get(day_input.lower().strip())


def normalize_meal_type(meal_input: str) -> str | None:
    """
    Normalizes a meal type to the internal format (English).
    Returns None if not recognized.
    """
    if not meal_input:
        return None
    return MEAL_TYPE_MAP.get(meal_input.lower().strip())


def get_day_display_name(day_num: int) -> str:
    """Gets the day name to display to the user (in Spanish)."""
    return DAYS_NUM_TO_NAME.get(day_num, f"día {day_num}")


def get_meal_type_display(meal_type: str) -> str:
    """Gets the meal type name to display to the user (in Spanish)."""
    meal_type_lower = meal_type.lower() if meal_type else ""
    return MEAL_TYPE_TO_DISPLAY.get(meal_type_lower, meal_type_lower)


def get_meal_type_value(meal_type) -> str:
    """
    Extracts the string value from meal_type, whether it's an enum or a string.
    Useful when meal_type may come as a SQLAlchemy enum.
    """
    if hasattr(meal_type, 'value'):
        return meal_type.value.lower()
    return str(meal_type).lower() if meal_type else ""