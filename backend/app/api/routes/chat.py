from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.agent.executor import agent_manager
from app.services.profile import ProfileService
from app.api.deps import get_current_user
from app.models.user import User
from app.services.agent.schemas import AgentResponse, ChatPayload, Suggestion

router = APIRouter()
@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(payload: ChatPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Recuperar el perfil y convertirlo a dict
    profile_obj = ProfileService.get_user_profile(db, current_user.id)
    if hasattr(profile_obj, 'dict'):
        profile_data = profile_obj.dict()
    else:
        # fallback para SQLAlchemy
        profile_data = {c: getattr(profile_obj, c, None) for c in dir(profile_obj) if not c.startswith('_') and not callable(getattr(profile_obj, c, None))}
    profile_data['user_id'] = current_user.id

    # Construir el agente
    agent = agent_manager.build_agent(profile_data)

    # Preparar mensajes
    messages = []
    if payload.history:
        for msg in payload.history:
            messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": payload.message})

    try:
        response = await agent.ainvoke({"messages": messages})
        # Extraer el texto del último mensaje AIMessage
        ai_text = None
        if response and "messages" in response and len(response["messages"]) > 0:
            last_message = response["messages"][-1]
            if hasattr(last_message, 'content'):
                ai_text = last_message.content
            elif isinstance(last_message, dict) and 'content' in last_message:
                ai_text = last_message['content']
            else:
                ai_text = str(last_message)
        else:
            ai_text = "Lo siento, no pude procesar tu solicitud."
        # Sugerencia opcional
        suggestion = None
        keywords = ["receta", "plato", "comida", "desayuno", "almuerzo", "cena"]
        if ai_text and any(keyword in ai_text.lower() for keyword in keywords):
            # suggestion debe ser un dict o instancia de Suggestion, no un string
            # Aquí solo ponemos un ejemplo dummy, deberías ajustar según tu lógica real
            suggestion = Suggestion(meal_detail_id=0, recipe_id=0, status=False)
        #return response
        return AgentResponse(text=ai_text, suggestion=suggestion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el agente: {str(e)}")