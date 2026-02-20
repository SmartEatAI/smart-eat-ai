from app.schemas.category import CategoryBase
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import eating_style as crud
from app.models import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/eating_style", tags=["Eating Style"])

@router.post("/", response_model=CategoryBase)
def create_eating_style(
    eating_style_in: CategoryBase, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    # Verificamos si ya tiene perfil
    existing = crud.existing_eating_style(db, name=eating_style_in.name)
    if existing:        
        return crud.add_eating_style_to_profile(db, eating_style_id=existing.id, profile_id=current_user.profile.id)
    return crud.create_eating_style_for_profile(db, obj_in=eating_style_in, profile_id=current_user.profile.id)