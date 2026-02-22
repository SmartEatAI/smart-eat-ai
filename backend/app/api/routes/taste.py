from app.schemas.category import CategoryBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import taste as crud

router = APIRouter(prefix="/taste")

@router.get("/", response_model=list[CategoryBase])
def read_tastes(
    db: Session = Depends(get_db), 
):
    return crud.get_tastes(db)