from fastapi import APIRouter, Depends, HTTPException
from app.services.agent.executor import agent_manager
from app.services.profile import ProfileService  # Tu service existente
from app.services.agent.prompts import get_nutritionist_prompt
from app.api.deps import get_current_user


router = APIRouter()

@router.post("/chat")
async def chat_with_agent(
    payload: dict, 
    current_user = Depends(get_current_user)
):
    user_id = current_user.id
    user_message = payload.get("message")
    chat_history = payload.get("history", [])

    # Recuperamos el perfil actualizado
    profile_data = await ProfileService.get_user_profile(user_id)
    
    # Preparamos el agente con el prompt personalizado
    system_prompt = get_nutritionist_prompt(profile_data)
    executor = agent_manager.get_executor()
    
    # Ejecutamos el agente (ReAct)
    # Combinamos el historial con el nuevo mensaje
    input_data = {
        "input": user_message,
        "chat_history": chat_history,
        "system_instructions": system_prompt
    }
    
    try:
        response = executor.invoke(input_data)
        return {
            "status": "success",
            "answer": response["output"],
            "suggestion": response.get("suggestion") # Si el agente generó una
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))