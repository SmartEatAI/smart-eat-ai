from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.agent.executor import agent_manager
from app.services.profile import ProfileService
from app.api.deps import get_current_user
from app.models.user import User
from app.services.agent.schemas import AgentResponse, ChatPayload, Suggestion

router = APIRouter()

def profile_to_dict(profile_obj):
    if hasattr(profile_obj, 'dict'):
        return profile_obj.dict()
    return {c: getattr(profile_obj, c, None) for c in dir(profile_obj) if not c.startswith('_') and not callable(getattr(profile_obj, c, None))}

def parse_agent_response(response):
    if response and "messages" in response and len(response["messages"]) > 0:
        last_message = response["messages"][-1]
        if hasattr(last_message, 'content'):
            return last_message.content
        elif isinstance(last_message, dict) and 'content' in last_message:
            return last_message['content']
        else:
            return str(last_message)
    return "Lo siento, no pude procesar tu solicitud."

@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(payload: ChatPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile_obj = ProfileService.get_user_profile(db, current_user.id)
    profile_data = profile_to_dict(profile_obj)
    profile_data['user_id'] = current_user.id

    agent = agent_manager.build_agent(profile_data)

    messages = [{"role": msg.role, "content": msg.content} for msg in payload.history] if payload.history else []
    messages.append({"role": "user", "content": payload.message})

    try:
        response = await agent.ainvoke({"messages": messages})
        ai_text = parse_agent_response(response)
        suggestion = None
        keywords = ["receta", "plato", "comida", "desayuno", "almuerzo", "cena"]
        if ai_text and any(keyword in ai_text.lower() for keyword in keywords):
            suggestion = Suggestion(meal_detail_id=0, recipe_id=0, status=False)
        return AgentResponse(text=ai_text, suggestion=suggestion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el agente: {str(e)}")