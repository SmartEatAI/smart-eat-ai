from app.schemas.category import CategoryBase
from app.crud.profile import get_profile
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.taste import Taste
from app.models.profile import Profile

def existing_taste(db: Session, name: str):
    """Verifica si ya existe un gusto con el mismo nombre."""
    try:
        return db.query(Taste).filter(Taste.name == name.lower()).first()
    except Exception as e:
        print(f"Error al verificar gusto existente: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Error interno al consultar los gustos en la base de datos"
        )

def get_tastes(db: Session):
    """Obtiene todas los gustos de la base de datos."""
    try:
        return db.query(Taste).all()
    except Exception as e:
        print(f"Error al obtener gustos: {str(e)}")
        
        raise HTTPException(
            status_code=500, 
            detail="Error interno al consultar los gustos en la base de datos"
        )

def get_taste_by_id(db: Session, taste_id: int):
    """"Obtiene un gusto por su ID."""
    try:
        return db.query(Taste).filter(Taste.id == taste_id).first()
    except Exception as e:
        print(f"Error al obtener gusto por ID: {str(e)}")
        
        raise HTTPException(
            status_code=500, 
            detail="Error interno al consultar los gustos en la base de datos"
        )

def get_tastes_by_profile(db: Session, profile_id: int):
    """Obtiene todos los gustos asociados a un perfil específico."""
    try:
        # Buscamos el perfil
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        
        if not profile:
            return []
            
        # Retornamos la lista de gustos vinculados al perfil
        return profile.tastes
        
    except Exception as e:
        print(f"Error al obtener gustos: {e}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

def create_taste_for_profile(db: Session, obj_in: CategoryBase, profile_id: int):
    """Crea un nuevo gusto y lo asocia a un perfil específico."""

    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    # Creamos la restricción sin user_id
    data = obj_in.model_dump()
    db_taste = Taste(**data)

    try:
        # Al añadirla a la lista SQLAlchemy crea el registro en la tabla intermedia automáticamente
        db_profile.tastes.append(db_taste)
        
        db.add(db_taste)
        db.commit()
        db.refresh(db_taste)
        return db_taste
    
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al asociar gusto")

def add_taste_to_profile(db: Session, taste_id: int, profile_id: int):
    """Asocia un gusto existente a un perfil específico."""

    # Buscamos el perfil y el gusto
    profile = get_profile(db, user_id=profile_id)
    taste = get_taste_by_id(db, taste_id=taste_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    
    if not taste:
        raise HTTPException(status_code=404, detail="Gusto no encontrado")
    
    # Verificamos si el gusto ya está asociado al perfil
    if taste in profile.tastes:
        raise HTTPException(status_code=400, detail="El gusto ya está asociado al perfil")
        
    try:
        # Asociamos el gusto al perfil
        profile.tastes.append(taste)
        db.commit()
        return taste
    
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al asociar gusto")