from app.schemas.category import CategoryBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.eating_style import EatingStyleService

router = APIRouter(prefix="/eating_style")

@router.get("/", response_model=list[CategoryBase])
def read_eating_styles(
    db: Session = Depends(get_db), 
):
    return EatingStyleService.list_eating_styles(db)