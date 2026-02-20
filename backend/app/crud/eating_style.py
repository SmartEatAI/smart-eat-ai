from app.schemas.category import CategoryBase
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.eating_style import EatingStyle
from app.models.profile import Profile


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