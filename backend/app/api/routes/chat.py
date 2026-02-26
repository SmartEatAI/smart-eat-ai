from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.agent.executor import agent_manager
from app.services.profile import ProfileService
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
    
    # Ejecutamos el agente (ReAct)
    # Combinamos el historial con el nuevo mensaje
    input_data = {
        "input": user_message,
        "chat_history": chat_history,
    }
    
    try:
        executor = agent_manager.build_agent(profile_data)

        response = await executor.ainvoke(input_data)

        # Extraer el texto del último mensaje AIMessage
        messages = response.get("messages", [])
        ai_text = None
        for msg in reversed(messages):
            if msg.__class__.__name__ == "AIMessage":
                ai_text = getattr(msg, "content", None)
                if ai_text:
                    break
        if not ai_text:
            ai_text = str(response)

        # Extraer suggestion si existe
        suggestion = response.get("suggestion") if isinstance(response, dict) else None

        return {
            "text": ai_text,
            "suggestion": suggestion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))