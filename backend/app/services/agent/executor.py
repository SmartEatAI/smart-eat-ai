from app.core.config_ollama import llm
from app.services.agent.tools import nutrition_tools
from app.services.agent.prompts import get_nutritionist_prompt
from app.services.agent.schemas import DietGraphState
from langgraph.prebuilt import ToolNode

from langchain_core.messages import AIMessage, HumanMessage


class AgentManager:
    def __init__(self):
        self.llm = llm.bind_tools(nutrition_tools)

    def build_agent(self, state: DietGraphState):
        """
        Construye el agente dinámicamente con el prompt personalizado basado en el perfil del usuario.
        """
        profile = state["profile"]
        active_plan = state["active_plan"]

        system_prompt = get_nutritionist_prompt(
                            profile=profile, 
                            active_plan=active_plan,
                            )
        
        # Preparar mensajes
        messages = [{"role": "system", "content": system_prompt}]
        
        # Añadir mensajes de la conversación
        for msg in state["messages"]:
            if isinstance(msg, HumanMessage):
                messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                messages.append({"role": "assistant", "content": msg.content})
        
        
        response = llm.invoke([{"role": "system", "content": system_prompt}] + state["messages"])

        return {"messages": [response]}

agent = AgentManager()