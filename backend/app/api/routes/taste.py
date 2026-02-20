from app.schemas.category import CategoryBase
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import taste as crud
from app.models import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/taste", tags=["Taste"])

@router.post("/", response_model=CategoryBase)
def create_taste(
    taste_in: CategoryBase, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    # Verificamos si ya tiene gustos
    existing = crud.existing_taste(db, name=taste_in.name)
    if existing:
        return crud.add_taste_to_profile(db, taste_id=existing.id, profile_id=current_user.profile.id)
    return crud.create_taste_for_profile(db, obj_in=taste_in, profile_id=current_user.profile.id)