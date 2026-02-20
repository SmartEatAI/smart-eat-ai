from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.profile_eating_style import ProfileEatingStyle
from app.models.taste import Taste
from app.models.restriction import Restriction
from app.schemas.profile import ProfileCreate, ProfileUpdate

def get_profile(db: Session, user_id: int):
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def update(db: Session, db_obj: Profile, obj_in: ProfileUpdate):
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