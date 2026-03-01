from app.core.config_ollama import llm
from app.services.agent.tools.tools import nutrition_tools
from app.services.agent.prompts import get_nutritionist_prompt
from app.services.agent.schemas import DietGraphState
import logging

logger = logging.getLogger(__name__)

class AgentManager:
    def __init__(self):
        self.llm = llm.bind_tools(nutrition_tools)
        self.tools = {tool.name: tool for tool in nutrition_tools}
        logger.info(f"🤖 Agente inicializado con {len(nutrition_tools)} herramientas")

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
        
        response = self.llm.invoke([{"role": "system", "content": system_prompt}] + state["messages"])

        return {"messages": [response]}

agent = AgentManager()