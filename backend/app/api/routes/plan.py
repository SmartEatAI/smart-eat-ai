from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.plan import PlanBase, PlanResponse
from app.services.plan import PlanService
from app.models import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/plan")

@router.get("/current", response_model=PlanResponse)
def get_current_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    return PlanService.get_current_plan(db, user_id=current_user.id)

@router.post("/", response_model=PlanResponse)
def create_plan(
    plan_in: PlanBase, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    return PlanService.create_plan(db, obj_in=plan_in, user_id=current_user.id)