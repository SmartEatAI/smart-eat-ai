from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db
from app.api.deps import get_current_user
from app.services.agent.workflow import app_graph
from langchain_core.messages import HumanMessage
from app.services.profile import ProfileService
from app.services.plan import PlanService
from app.schemas.profile import ProfileResponse
from app.schemas.plan import PlanResponse


router = APIRouter(prefix="/chat")

@router.post("/")
async def send_message(
    message: str, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    ):

    # convertir el objeto ORM a Pydantic
    db_profile = ProfileService.get_user_profile(db, user.id)
    profile = ProfileResponse.model_validate(db_profile) 

    db_plan = PlanService.get_current_plan(db, user.id)
    active_plan = PlanResponse.model_validate(db_plan) if db_plan else None

    config = {
        "configurable": {
            "thread_id": user.id
        }
    }

    result = app_graph.invoke(
        {
            "messages": [HumanMessage(content=message)],
            "profile": profile,
            "active_plan": active_plan
        },
        config=config
    )

    return {
        "response": result["messages"][-1].content
    }