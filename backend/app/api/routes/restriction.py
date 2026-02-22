from app.schemas.category import CategoryBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import restriction as crud

router = APIRouter(prefix="/restriction")

@router.get("/", response_model=list[CategoryBase])
def read_restrictions(
    db: Session = Depends(get_db), 
):
    return crud.get_restrictions(db)
