from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from app.services.agent.tools import nutrition_tools
from app.services.agent.prompts import get_nutritionist_prompt


class AgentManager:
    def __init__(self):
        # Modelo LLM (Ollama local)
        self.llm = ChatOllama(
            model="llama3.1",
            base_url="http://ollama:11434",
            temperature=0
        )

        self.tools = nutrition_tools

        # El agente se construye dinámicamente porque el prompt depende del perfil
        self.agent = None
        self.agent_executor = None

    def build_agent(self, user_profile):
        """
        Construye el agente dinámicamente con el prompt personalizado
        basado en el perfil del usuario.
        """

        system_prompt = get_nutritionist_prompt(user_profile)

        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt
        )


        return self.agent


agent_manager = AgentManager()
