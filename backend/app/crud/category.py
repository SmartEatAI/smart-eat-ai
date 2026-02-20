from typing import Any, Type, List
from sqlalchemy.orm import Session

def get_or_create_category(db: Session, model: Type, name: str):
    """Busca una categoría por nombre (case-insensitive) o la crea si no existe."""
    name_low = name.strip().lower()
    instance = db.query(model).filter(model.name == name_low).first()
    if not instance:
        instance = model(name=name_low)
        db.add(instance)
        db.flush()  # Obtenemos el ID sin confirmar la transacción completa aún
    return instance

def process_profile_categories(db: Session, model: Type, items: List[Any]) -> List:
    """
    Procesa objetos CategoryUpdate. 
    Si traen ID, los busca; si no, busca por nombre o crea.
    """
    result_objects = []
    for item in items:
        # 'item' ahora es un objeto Pydantic o un diccionario
        item_data = item if isinstance(item, dict) else item.model_dump()
        
        obj_id = item_data.get("id")
        obj_name = item_data.get("name")

        if obj_id:
            # Reutilizamos tu lógica: Buscar por ID
            obj = db.query(model).get(obj_id)
            if obj:
                result_objects.append(obj)
        elif obj_name:
            # Reutilizamos tu lógica: Buscar o crear por nombre
            obj = get_or_create_category(db, model, obj_name)
            result_objects.append(obj)
            
    return result_objects