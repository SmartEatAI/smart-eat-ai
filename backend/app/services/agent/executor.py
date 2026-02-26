from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from app.services.agent.tools import search_recipes, update_user_preferences, get_current_user_plan

class AgentManager:
    def __init__(self):
        # Conectamos con el contenedor de Ollama definido en docker-compose
        self.llm = ChatOllama(
            model="llama3",
            base_url="http://ollama:11434",
            temperature=0  # Mantener bajo para evitar inventos nutricionales
        )
        
        # Lista de herramientas disponibles
        self.tools = [search_recipes, update_user_preferences, get_current_user_plan]
        
        # Descargamos un prompt estándar de ReAct (puedes personalizarlo en prompts.py)
        self.prompt = hub.pull("hwchase17/react")

    def get_executor(self):
        # Creamos el agente ReAct
        agent = create_react_agent(self.llm, self.tools, self.prompt)
        
        # El executor es el que maneja el ciclo de pensamiento
        return AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            verbose=True, 
            handle_parsing_errors=True
        )

agent_manager = AgentManager()