from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from app.services.agent.schemas import DietGraphState
from app.services.agent.executor import agent
from backend.app.services.agent.tools.tools import nutrition_tools

import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def should_continue(state: DietGraphState):
    messages = state["messages"]
    last_message = messages[-1]
    # Si el modelo hizo una "tool_call", vamos al nodo de herramientas
    if last_message.tool_calls:
        return "tools"
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