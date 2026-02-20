from backend.app.schemas.category import CategoryResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import restriction as crud
from app.models import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/restriction", tags=["Restriction"])

@router.post("/", response_model=CategoryResponse)
def create_restriction(
    restriction_in: CategoryResponse, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    # Verificamos si ya tiene perfil
    if crud.get_restrictions_by_profile(db, profile_id=current_user.profile.id):
        raise HTTPException(status_code=400, detail="El usuario ya tiene una restricción asociada.")
    
    return crud.create_restriction_for_profile(db, obj_in=restriction_in, profile_id=current_user.profile.id)