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
async def chat_with_agent(payload: ChatPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    # Obtener el perfil del usuario
    profile_data = ProfileService.get_user_profile(db, current_user.id)

    # Prompt personalizado
    system_prompt = get_nutritionist_prompt(profile_data)
    
    # Preparamos los inputs para LangChain / Agent
    # Convertimos el historial a un formato que el agente entienda si es necesario
    input_data = {
        "chat_history": payload.history,
        "system_instructions": system_prompt
    }
    
    try:
        # Agente - LangChain
        executor = agent_manager.build_agent(input_data)

        # Invocación del agente
        response = await executor.ainvoke({
            "input": payload.message
        })

        # Mapeo al esquema AgentResponse
        return AgentResponse(
            text=response.get("output", "No pude generar una respuesta."),
            # Intentamos extraer 'suggestion' si el agente la incluyó en el output
            suggestion=response.get("suggestion") 
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el agente: {str(e)}")