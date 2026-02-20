from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.restriction import Restriction
from app.schemas.restriction import RestrictionBase
from app.models.profile import Profile


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

def create_restriction_for_profile(db: Session, obj_in: RestrictionBase, profile_id: int):
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