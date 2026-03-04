from app.core.config_ollama import llm
from app.services.agent.tools.tools import nutrition_tools
from app.services.agent.prompts import get_nutritionist_prompt
from app.services.agent.schemas import DietGraphState
from app.services.agent.memory import (
    optimize_state_for_inference,
    get_state_stats,
    MAX_CONTEXT_TOKENS
)
import logging

# Importaciones para acortar tokens de mensajes en caso de pasarse
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import count_tokens_approximately

logger = logging.getLogger(__name__)

# Configuración optimizada para 8GB VRAM - alineado con MAX_CONTEXT_TOKENS en memory.py
MAX_TOKENS_FOR_HISTORY = MAX_CONTEXT_TOKENS


class AgentManager:
    def __init__(self):
        self.llm = llm.bind_tools(nutrition_tools)
        self.tools = {tool.name: tool for tool in nutrition_tools}
        logger.info(f"🤖 Agente inicializado con {len(nutrition_tools)} herramientas")

    def build_agent(self, state: DietGraphState):
        """
        Dynamically builds the agent with a customized prompt based on the user's profile.
        Optimized to reduce latency on GPUs with limited memory.
        """
        # Paso 1: Optimizar estado (comprime tool results si es necesario)
        optimized_state = optimize_state_for_inference(state)
        profile = optimized_state["profile"]
        messages = optimized_state["messages"]

        # Paso 2: Aplicar trim de mensajes como última línea de defensa
        trimmed_messages = trim_messages(
            messages,
            max_tokens=MAX_TOKENS_FOR_HISTORY,
            strategy="last",
            token_counter=count_tokens_approximately,
            start_on="human",
            end_on=("human", "tool"),
            include_system=False,
        )

        system_prompt = get_nutritionist_prompt(
                            profile=profile, 
                            )
        
        # Log de diagnóstico
        stats = get_state_stats({"messages": trimmed_messages})
        logger.debug(f"📊 Estado: {stats['total_messages']} msgs, {stats['total_tokens']} tokens, tools: {stats['tool_calls']}")
        
        response = self.llm.invoke([{"role": "system", "content": system_prompt}] + trimmed_messages)
        
        # Advertencia si respuesta vacía
        if not response.content and not (hasattr(response, 'tool_calls') and response.tool_calls):
            logger.warning("⚠️ Respuesta vacía del modelo")

        return {"messages": [response]}

agent = AgentManager()