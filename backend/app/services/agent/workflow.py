from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.services.agent.schemas import DietGraphState
from app.services.agent.executor import agent
from app.services.agent.tools import nutrition_tools
from langgraph.prebuilt import ToolNode
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def should_continue(state: DietGraphState):
    messages = state["messages"]
    last_message = messages[-1]
    # Si el modelo hizo una "tool_call", vamos al nodo de herramientas
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        logger.info(f"🔧 Ejecutando tool: {last_message.tool_calls[0]['name']}")
        return "tools"
    
    # Verificar si el mensaje contiene indicadores de que debería usar una tool
    content = last_message.content.lower() if hasattr(last_message, 'content') else ""
    
    # Palabras clave que deberían activar tools
    tool_triggers = [
        "buscar", "encuentra", "necesito un plan", "genera un plan", "crea un plan",
        "cambia", "reemplaza", "sugiere", "alternativa", "otra opción",
        "no me gusta", "soy alérgico", "no como", "odia", "detesta",
        "ver plan", "ver perfil", "muéstrame", "qué tengo"
    ]
    
    for trigger in tool_triggers:
        if trigger in content:
            logger.info(f"⚠️ El mensaje debería usar tool pero no lo hizo. Trigger: '{trigger}'")
            # Aquí podrías forzar una respuesta específica o simplemente continuar
            break
    
    return END


def route_after_tools(state: DietGraphState):
    """Determina si después de las tools volvemos al agente o terminamos"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Si el último mensaje es de tool, siempre volvemos al agente para procesar el resultado
    if hasattr(last_message, 'type') and last_message.type == 'tool':
        logger.info("📤 Tool ejecutada, volviendo al agente")
        return "nutricionista"
    
    return END



def build_graph():
    tool_node = ToolNode(nutrition_tools)

    workflow = StateGraph(DietGraphState)

    # Nodos
    workflow.add_node("nutricionista", agent.build_agent)
    workflow.add_node("tools", tool_node)

    # Flujo
    workflow.set_entry_point("nutricionista")

    workflow.add_conditional_edges("nutricionista", should_continue, {
            "tools": "tools",
            END: END
        })
    
    workflow.add_edge("tools", "nutricionista") # Vuelve al agente para confirmar la acción

    checkpointer = MemorySaver()

    return workflow.compile(checkpointer=checkpointer)

app_graph = build_graph()