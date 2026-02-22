from sqlalchemy.orm import Session
from app.models.taste import Taste
from app.models.profile import Profile
from app.schemas.category import CategoryBase

def existing_taste(db: Session, name: str):
    return db.query(Taste).filter(Taste.name == name.lower()).first()

def get_tastes(db: Session):
    return db.query(Taste).all()

def get_taste_by_id(db: Session, taste_id: int):
    return db.query(Taste).filter(Taste.id == taste_id).first()

def get_tastes_by_profile(db: Session, profile_id: int):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        return []
    return profile.tastes

def create_taste_for_profile(db: Session, obj_in: CategoryBase, profile_id: int):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        return None
    data = obj_in.model_dump()
    db_taste = Taste(**data)
    db_profile.tastes.append(db_taste)
    db.add(db_taste)
    db.commit()
    db.refresh(db_taste)
    return db_taste

def add_taste_to_profile(db: Session, taste_id: int, profile_id: int):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    taste = db.query(Taste).filter(Taste.id == taste_id).first()
    if not profile or not taste:
        return None
    if taste in profile.tastes:
        return None
    profile.tastes.append(taste)
    db.commit()
    return taste