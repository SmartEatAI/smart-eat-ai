from app.core.config_ollama import llm
from app.services.agent.tools.tools import nutrition_tools
from app.services.agent.prompts import get_nutritionist_prompt
from app.services.agent.schemas import DietGraphState
import logging

# Importaciones para acortar tokens de mensajes en caso de pasarse
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import count_tokens_approximately

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

        trimmed_messages = trim_messages(
            state["messages"],
            max_tokens=10000,
            strategy="last",
            token_counter=count_tokens_approximately,
            start_on="human",
            end_on=("human", "tool"),
        )

        system_prompt = get_nutritionist_prompt(
                            profile=profile, 
                            )
        
        response = self.llm.invoke([{"role": "system", "content": system_prompt}] + trimmed_messages)

        return {"messages": [response]}

agent = AgentManager()