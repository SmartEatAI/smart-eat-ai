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
    if crud.get_tastes_by_profile(db, profile_id=current_user.profile.id):
        raise HTTPException(status_code=400, detail="The user already has that taste.")
    
    return crud.create_taste_for_profile(db, obj_in=taste_in, profile_id=current_user.profile.id)