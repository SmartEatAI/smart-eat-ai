from app.schemas.category import CategoryBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import eating_style as crud

router = APIRouter(prefix="/eating_style", tags=["Eating Style"])


@router.get("/", response_model=list[CategoryBase])
def read_eating_styles(
    db: Session = Depends(get_db), 
):
    return crud.get_eating_styles(db)

