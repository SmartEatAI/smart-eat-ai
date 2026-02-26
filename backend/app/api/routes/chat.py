from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.agent.executor import agent_manager
from app.services.profile import ProfileService
from app.services.agent.prompts import get_nutritionist_prompt
from app.api.deps import get_current_user
from app.models.user import User
from app.services.agent.schemas import AgentResponse, ChatPayload



router = APIRouter()

@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(
    payload: ChatPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    user_message = payload.message
    chat_history = payload.history

    # Recuperamos el perfil actualizado
    profile_data = ProfileService.get_user_profile(db, user_id)
    
    # Preparamos el agente con el prompt personalizado
    system_prompt = get_nutritionist_prompt(profile_data)
    
    # Ejecutamos el agente (ReAct)
    # Combinamos el historial con el nuevo mensaje
    input_data = {
        "input": user_message,
        "chat_history": chat_history,
        "system_instructions": system_prompt
    }
    
    try:
        executor = agent_manager.build_agent(profile_data)

        response = await executor.ainvoke({
            "messages": [
                {"role": "user", "content": user_message}
            ]
        })

        return {
            "status": "success",
            "answer": response["output"],
            "suggestion": response.get("suggestion") # Si el agente generó una
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))