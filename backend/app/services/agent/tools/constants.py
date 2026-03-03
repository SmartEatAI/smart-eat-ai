"""
Constantes compartidas para las tools del agente nutricional.
Centraliza mapeos de días, tipos de comida y otras configuraciones.
"""

# Mapeo de días en español/inglés a números (ISO weekday: lunes=1)
DAYS_MAP = {
    # Español
    "lunes": 1, "martes": 2, "miércoles": 3, "miercoles": 3,
    "jueves": 4, "viernes": 5, "sábado": 6, "sabado": 6, "domingo": 7,
    # Inglés
    "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4,
    "friday": 5, "saturday": 6, "sunday": 7
}

# Mapeo inverso: número a nombre del día (español)
DAYS_NUM_TO_NAME = {
    1: "lunes", 2: "martes", 3: "miércoles", 4: "jueves",
    5: "viernes", 6: "sábado", 7: "domingo"
}

# Mapeo de tipos de comida en español a inglés (interno)
MEAL_TYPE_MAP = {
    # Español
    "desayuno": "breakfast", 
    "almuerzo": "lunch", 
    "comida": "lunch",
    "cena": "dinner", 
    "snack": "snack", 
    "merienda": "snack",
    # Inglés (para normalización)
    "breakfast": "breakfast", 
    "lunch": "lunch", 
    "dinner": "dinner"
}

# Mapeo inverso: inglés a español (para mostrar al usuario)
MEAL_TYPE_TO_DISPLAY = {
    "breakfast": "desayuno", 
    "lunch": "almuerzo", 
    "dinner": "cena", 
    "snack": "snack"
}


def normalize_day(day_input: str) -> int | None:
    """
    Normaliza un día de la semana a su número correspondiente.
    Retorna None si no se reconoce.
    """
    if not day_input:
        return None
    return DAYS_MAP.get(day_input.lower().strip())


def normalize_meal_type(meal_input: str) -> str | None:
    """
    Normaliza un tipo de comida al formato interno (inglés).
    Retorna None si no se reconoce.
    """
    if not meal_input:
        return None
    return MEAL_TYPE_MAP.get(meal_input.lower().strip())


def get_day_display_name(day_num: int) -> str:
    """Obtiene el nombre del día para mostrar al usuario."""
    return DAYS_NUM_TO_NAME.get(day_num, f"día {day_num}")


def get_meal_type_display(meal_type: str) -> str:
    """Obtiene el nombre del tipo de comida para mostrar al usuario."""
    meal_type_lower = meal_type.lower() if meal_type else ""
    return MEAL_TYPE_TO_DISPLAY.get(meal_type_lower, meal_type_lower)


def get_meal_type_value(meal_type) -> str:
    """
    Extrae el valor string del meal_type, sea enum o string.
    Útil cuando meal_type puede venir como enum de SQLAlchemy.
    """
    if hasattr(meal_type, 'value'):
        return meal_type.value.lower()
    return str(meal_type).lower() if meal_type else ""
