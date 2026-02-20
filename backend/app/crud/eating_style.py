from app.schemas.category import CategoryBase
from app.crud.profile import get_profile
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.eating_style import EatingStyle
from app.models.profile import Profile

def existing_eating_style(db: Session, name: str):
    """Verifica si ya existe un estilo de alimentación con el mismo nombre."""
    try:
        return db.query(EatingStyle).filter(EatingStyle.name == name.lower()).first()
    except Exception as e:
        print(f"Error al verificar estilo de alimentación existente: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Error interno al consultar los estilos de alimentación en la base de datos"
        )

def get_eating_styles(db: Session):
    """Obtiene todas los estilos de alimentación de la base de datos."""
    try:
        return db.query(EatingStyle).all()
    except Exception as e:
        print(f"Error al obtener estilos de alimentación: {str(e)}")
        
        raise HTTPException(
            status_code=500, 
            detail="Error interno al consultar los estilos de alimentación en la base de datos"
        )

def get_eating_style_by_id(db: Session, eating_style_id: int):
    """"Obtiene un estilo de alimentación por su ID."""
    try:
        return db.query(EatingStyle).filter(EatingStyle.id == eating_style_id).first()
    except Exception as e:
        print(f"Error al obtener estilo de alimentación por ID: {str(e)}")
        
        raise HTTPException(
            status_code=500, 
            detail="Error interno al consultar los estilos de alimentación en la base de datos"
        )

def get_eating_styles_by_profile(db: Session, profile_id: int):
    """Obtiene todos los estilos de alimentación asociados a un perfil específico."""
    try:
        # Buscamos el perfil
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        
        if not profile:
            return []
            
        # Retornamos la lista de estilos de alimentación vinculados al perfil
        return profile.eating_styles
        
    except Exception as e:
        print(f"Error al obtener estilos de alimentación: {e}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

def create_eating_style_for_profile(db: Session, obj_in: CategoryBase, profile_id: int):
    """Crea un nuevo estilo de alimentación y lo asocia a un perfil específico."""

    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    # Creamos la restricción sin user_id
    data = obj_in.model_dump()
    db_eating_style = EatingStyle(**data)

    try:
        # Al añadirla a la lista SQLAlchemy crea el registro en la tabla intermedia automáticamente
        db_profile.eating_styles.append(db_eating_style)
        
        db.add(db_eating_style)
        db.commit()
        db.refresh(db_eating_style)
        return db_eating_style
    
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al asociar gusto")
    
def add_eating_style_to_profile(db: Session, eating_style_id: int, profile_id: int):
    """Asocia un estilo de alimentación existente a un perfil específico."""

    # Buscamos el perfil y el estilo de alimentación
    profile = get_profile(db, user_id=profile_id)
    eating_style = get_eating_style_by_id(db, eating_style_id=eating_style_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    
    if not eating_style:
        raise HTTPException(status_code=404, detail="Estilo de alimentación no encontrado")
    
    print(f"Perfil: {profile}, Estilo de alimentación: {eating_style}")
    # Verificamos si el estilo de alimentación ya está asociado al perfil
    if eating_style in profile.eating_styles:
        raise HTTPException(status_code=400, detail="El estilo de alimentación ya está asociado al perfil")
        
    try:
        # Asociamos el estilo de alimentación al perfil
        profile.eating_styles.append(eating_style)
        db.commit()
        return eating_style
    
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al asociar estilo de alimentación")