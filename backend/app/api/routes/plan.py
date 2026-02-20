from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.plan import PlanBase, PlanResponse
from app.crud import plan as crud
from app.models import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/plan", tags=["Plan"])

@router.get("/current", response_model=PlanResponse)
def get_current_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    return crud.get_plan_by_current_user(db, user_id=current_user.id)

@router.post("/", response_model=PlanResponse)
def create_plan(
    plan_in: PlanBase, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    return crud.create_plan(db, obj_in=plan_in, user_id=current_user.id)

@router.put("/{plan_id}/status", response_model=PlanResponse)
def update_plan_status(
    plan_id: int, 
    active: bool, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    return crud.update_plan_status(db, plan_id=plan_id, active=active)