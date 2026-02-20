from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.profile import ProfileCreate, ProfileResponse
from app.models import User
from app.api.deps import get_current_user
from app.crud.profile import get_profile

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=ProfileResponse)
def read_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    profile = get_profile(db, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return profile

