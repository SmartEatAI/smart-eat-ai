from typing import List
from app.models.taste import Taste
from app.models.restriction import Restriction
from sqlalchemy.orm import Session
from fastapi import HTTPException

def get_or_create_category(db: Session, model: Taste | Restriction, name: str):
    """Busca una categoría por nombre (case-insensitive) o la crea si no existe."""
    try:
        name_low = name.strip().lower()
        instance = db.query(model).filter(model.name == name_low).first()
        if not instance:
            instance = model(name=name_low)
            db.add(instance)
            db.flush()  # Obtenemos el ID sin confirmar la transacción completa aún
        return instance
    except Exception as e:
        print(f"Database error when getting_or_create_category: {e}")
        raise HTTPException(status_code=500, detail="Database error when getting_or_create_category")

def process_categories(db: Session, model: Taste | Restriction, items: List[Taste | Restriction]) -> List:
    """
    Procesa objetos CategoryUpdate. 
    Si traen ID, los busca; si no, busca por nombre o crea.
    """
    try:
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
    except Exception as e:
        print(f"Database error when process_profile_categories: {e}")
        raise HTTPException(status_code=500, detail="Database error when process_profile_categories")