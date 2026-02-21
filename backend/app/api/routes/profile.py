from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.profile import ProfileBase, ProfileCreate, ProfileResponse
from app.models import User
from app.api.deps import get_current_user
from app.crud.profile import create_user_profile, update_user_profile, get_profile

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=ProfileResponse)
def read_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    profile = get_profile(db, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not existing.")
    return profile

@router.post("/", response_model=ProfileResponse)
def create_profile(
    profile_in: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    existing_profile = get_profile(db, user_id=current_user.id)
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists.")
    
    profile = create_user_profile(db, obj_in=profile_in, user_id=current_user.id)
    return profile

@router.put("/", response_model=ProfileResponse)
def update_profile(
    profile_in: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    profile = update_user_profile(db, obj_in=profile_in, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not existing.")

    return profile