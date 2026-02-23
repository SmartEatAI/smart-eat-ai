from app.schemas.category import CategoryBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.eating_style import EatingStyleService
from app.services.diet_type import DietTypeService

router = APIRouter(prefix="/diet_type")

@router.get("/", response_model=list[CategoryBase])
def read_diet_types(
    db: Session = Depends(get_db), 
):
    return DietTypeService.list_diet_types(db)