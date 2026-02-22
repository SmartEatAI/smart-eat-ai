from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.profile import ProfileCreate, ProfileResponse
from app.models import User
from app.api.deps import get_current_user
from app.services.profile import ProfileService

router = APIRouter(prefix="/profile")

@router.get("/", response_model=ProfileResponse)
def read_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    profile = ProfileService.get_user_profile(db, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not existing.")
    return profile

@router.put("/", response_model=ProfileResponse)
def upsert_profile(
    profile_in: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    profile = ProfileService.upsert_user_profile(db, obj_in=profile_in, user_id=current_user.id)
    return profile