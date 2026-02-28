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
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat")

@router.post("/")
async def send_message(
    message: str, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    ):
    
    # Log para debugging
    logger.info(f"Usuario {user.id} envió: {message}")

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

    try:
        # Inyectar el user_id en el mensaje para que el agente lo tenga siempre presente
        enhanced_message = f"[USER_ID: {user.id}] {message}"

        result = app_graph.invoke(
            {
                "messages": [HumanMessage(content=message)],
                "profile": profile,
                "active_plan": active_plan
            },
            config=config
        )

        last_message = result["messages"][-1]
        
        # Verificar si el agente usó tools
        used_tools = []
        for msg in result["messages"]:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    used_tools.append(tool_call['name'])
        
        logger.info(f"Tools usadas: {used_tools if used_tools else 'NINGUNA - POSIBLE PROBLEMA'}")
        
        return {
            "response": last_message.content,
            "used_tools": used_tools if used_tools else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el asistente: {str(e)}")