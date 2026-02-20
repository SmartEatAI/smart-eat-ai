from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.taste import Taste
from app.models.restriction import Restriction
from app.schemas.profile import ProfileCreate, ProfileUpdate

def get_profile(db: Session, user_id: int):
    """Obtiene el perfil asociado a un usuario específico."""
    return db.query(Profile).filter(Profile.user_id == user_id).first()

def create(db: Session, obj_in: ProfileCreate, user_id: int):
    """Crea un nuevo perfil para un usuario específico."""
    try:
        db_profile = Profile(**obj_in.model_dump(), user_id=user_id)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile
    except Exception as e:
        db.rollback()
        raise e

def update(db: Session, db_obj: Profile, obj_in: ProfileUpdate):
    """Actualiza un perfil existente con los datos proporcionados."""
    # Convertimos los datos de entrada a diccionario ignorando los valores no enviados (None)
    update_data = obj_in.dict(exclude_unset=True)
    
    # Manejo especial para relaciones si se incluyen en el update
    if "taste_ids" in update_data:
        ids = update_data.pop("taste_ids")
        db_obj.tastes = db.query(Taste).filter(Taste.id.in_(ids)).all()
        
    if "restriction_ids" in update_data:
        ids = update_data.pop("restriction_ids")
        db_obj.restrictions = db.query(Restriction).filter(Restriction.id.in_(ids)).all()

    # Actualizar campos directos (peso, altura, etc.)
    for field in update_data:
        setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj