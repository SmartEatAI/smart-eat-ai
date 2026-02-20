from app.schemas.category import CategoryBase
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import restriction as crud
from app.models import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/restriction", tags=["Restriction"])

@router.post("/", response_model=CategoryBase)
def create_restriction(
    restriction_in: CategoryBase, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    # Verificamos si ya tiene restricciones
    if crud.get_restrictions_by_profile(db, profile_id=current_user.profile.id):
        raise HTTPException(status_code=400, detail="The user already has that restriction.")
    
    return crud.create_restriction_for_profile(db, obj_in=restriction_in, profile_id=current_user.profile.id)