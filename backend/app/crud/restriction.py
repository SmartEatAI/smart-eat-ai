from app.schemas.category import CategoryBase
from app.crud.profile import get_profile
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.restriction import Restriction
from app.models.profile import Profile

def existing_restriction(db: Session, name: str):
    """Verifica si ya existe una restricción con el mismo nombre."""
    try:
        return db.query(Restriction).filter(Restriction.name == name.lower()).first()
    except Exception as e:
        print(f"Error al verificar restricción existente: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Error interno al consultar las restricciones en la base de datos"
        )

def get_restrictions(db: Session):
    """Obtiene todas las restricciones de la base de datos."""
    try:
        return db.query(Restriction).all()
    except Exception as e:
        print(f"Error al obtener restricciones: {str(e)}")
        
        raise HTTPException(
            status_code=500, 
            detail="Error interno al consultar las restricciones en la base de datos"
        )

def get_restriction_by_id(db: Session, restriction_id: int):
    """"Obtiene una restricción por su ID."""
    try:
        return db.query(Restriction).filter(Restriction.id == restriction_id).first()
    except Exception as e:
        print(f"Error al obtener restricción por ID: {str(e)}")
        
        raise HTTPException(
            status_code=500, 
            detail="Error interno al consultar las restricciones en la base de datos"
        )

def get_restrictions_by_profile(db: Session, profile_id: int):
    """Obtiene todas las restricciones asociadas a un perfil específico."""
    try:
        # Buscamos el perfil
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        
        if not profile:
            return []
            
        # Retornamos la lista de restricciones vinculadas al perfil
        return profile.restrictions
        
    except Exception as e:
        print(f"Error al obtener restricciones: {e}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

def create_restriction_for_profile(db: Session, obj_in: CategoryBase, profile_id: int):
    """Crea una nueva restricción y la asocia a un perfil específico."""

    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    # Creamos la restricción sin user_id
    data = obj_in.model_dump()
    db_restriction = Restriction(**data)

    try:
        # Al añadirla a la lista SQLAlchemy crea el registro en la tabla intermedia automáticamente
        db_profile.restrictions.append(db_restriction)
        
        db.add(db_restriction)
        db.commit()
        db.refresh(db_restriction)
        return db_restriction
    
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al asociar restricción")
    
def add_restriction_to_profile(db: Session, restriction_id: int, profile_id: int):
    """Asocia una restricción existente a un perfil específico."""
    
    # Buscamos el perfil y la restricción
    profile = get_profile(db, user_id=profile_id)
    restriction = get_restriction_by_id(db, restriction_id=restriction_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    
    if not restriction:
        raise HTTPException(status_code=404, detail="Restricción no encontrada")
    
    # Verificamos si la restricción ya está asociada al perfil
    if restriction in profile.restrictions:
        raise HTTPException(status_code=400, detail="La restricción ya está asociada al perfil")
        
    try:
        # Asociamos la restricción al perfil
        profile.restrictions.append(restriction)
        db.commit()
        return restriction
    
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        
        raise HTTPException(status_code=500, detail="Error al asociar restricción")