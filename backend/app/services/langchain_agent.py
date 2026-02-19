"""
Servicio del agente LangChain para recomendaciones de recetas.
Configura el LLM, memory, tools y el agente conversacional.
"""

from typing import Optional, List
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama
from sqlalchemy.orm import Session
import logging

from app.services.langchain_tools import (
    SearchSimilarRecipesTool,
    GetRecipeDetailsTool,
    GetUserPlanTool,
    CompareNutritionalProfilesTool,
    UpdateMealInPlanTool
)

logger = logging.getLogger(__name__)


class LangChainAgentService:
    """Servicio singleton para gestionar el agente LangChain"""
    
    _instance = None
    _agent = None
    _memory = None
    _llm = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LangChainAgentService, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(
        cls, 
        ollama_base_url: str = "http://ollama:11434",
        model_name: str = "mistral",
        temperature: float = 0.7
    ):
        """
        Inicializa el agente LangChain con todas sus dependencias.
        
        Args:
            ollama_base_url: URL del servidor Ollama
            model_name: Nombre del modelo a usar (mistral, llama2, etc.)
            temperature: Temperatura para generación (0-1)
        """
        try:
            # Inicializar LLM con Ollama
            cls._llm = Ollama(
                model=model_name,
                base_url=ollama_base_url,
                temperature=temperature
            )
            logger.info(f"LLM Ollama inicializado: {model_name} @ {ollama_base_url}")
            
            # Configurar memoria conversacional
            cls._memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="output"
            )
            logger.info("Memory inicializada")
            
            # TODO: Inicializar tools (necesitan db_session en runtime)
            # Las tools se inyectarán cuando se use el agente
            
            cls._initialized = True
            logger.info("LangChain Agent Service inicializado correctamente")
            
        except Exception as e:
            logger.error(f"Error inicializando LangChain Agent: {e}")
            cls._initialized = False
            raise
    
    @classmethod
    def is_initialized(cls) -> bool:
        """Verifica si el agente está inicializado"""
        return cls._initialized
    
    @classmethod
    def create_agent(cls, db_session: Session):
        """
        Crea una instancia del agente con las tools configuradas.
        Debe llamarse en cada request para inyectar la sesión de BD.
        
        Args:
            db_session: Sesión de SQLAlchemy para las tools
            
        Returns:
            Agente LangChain configurado
        """
        if not cls._initialized:
            raise RuntimeError("Agent no inicializado. Llamar a initialize() primero.")
        
        # Crear tools con sesión de BD inyectada
        tools = [
            SearchSimilarRecipesTool(db_session=db_session),
            GetRecipeDetailsTool(db_session=db_session),
            GetUserPlanTool(db_session=db_session),
            CompareNutritionalProfilesTool(db_session=db_session),
            UpdateMealInPlanTool(db_session=db_session)
        ]
        
        # Crear agente con tipo ZERO_SHOT_REACT_DESCRIPTION
        agent = initialize_agent(
            tools=tools,
            llm=cls._llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=cls._memory,
            verbose=True,  # TODO: Cambiar a False en producción
            max_iterations=5,
            early_stopping_method="generate",
            handle_parsing_errors=True
        )
        
        return agent
    
    @classmethod
    def get_system_prompt(cls) -> str:
        """
        Retorna el prompt del sistema para el agente.
        Define el rol, capacidades y formato de respuesta.
        """
        return """
        Eres un asistente nutricional experto especializado en recomendar recetas saludables.
        
        Tu objetivo es ayudar a los usuarios a mejorar sus planes alimenticios sugiriendo
        recetas alternativas que sean nutricionalmente similares pero que puedan ofrecer
        ventajas específicas (mejor balance de macros, menos calorías, más fibra, etc.).
        
        CAPACIDADES:
        - Buscar recetas similares usando un modelo de Machine Learning (KNN)
        - Analizar perfiles nutricionales de recetas
        - Comparar recetas y explicar diferencias
        - Actualizar planes semanales de usuarios
        
        INSTRUCCIONES:
        1. Cuando un usuario pida cambiar una receta, primero identifica qué receta quiere cambiar
        2. Usa la herramienta de búsqueda para encontrar alternativas similares
        3. Compara las opciones nutricionalmente
        4. Presenta UNA recomendación clara con justificación
        5. Si el usuario acepta, actualiza el plan
        
        FORMATO DE RESPUESTA:
        - Sé claro y conciso
        - Explica las ventajas nutricionales en términos simples
        - Usa porcentajes cuando compares valores
        - Enfócate en beneficios para la salud del usuario
        
        NUNCA hagas cambios sin confirmación del usuario.
        """
    
    @classmethod
    def run_agent(
        cls, 
        user_message: str, 
        db_session: Session,
        chat_history: Optional[List[dict]] = None,
        context: Optional[dict] = None
    ) -> dict:
        """
        Ejecuta el agente con un mensaje del usuario.
        
        Args:
            user_message: Mensaje del usuario
            db_session: Sesión de base de datos
            chat_history: Historial del chat [{"role": "user/assistant", "content": "..."}]
            context: Contexto adicional (plan_id, usuario_id, etc.)
            
        Returns:
            Dict con la respuesta del agente
        """
        try:
            # Crear agente con sesión de BD
            agent = cls.create_agent(db_session)
            
            # Limpiar memoria antes de ejecutar
            if cls._memory:
                cls._memory.clear()
            
            # Agregar historial del chat a la memoria si existe
            if chat_history:
                for msg in chat_history:
                    if msg.get("role") == "user":
                        cls._memory.chat_memory.add_user_message(msg.get("content", ""))
                    elif msg.get("role") == "assistant":
                        cls._memory.chat_memory.add_ai_message(msg.get("content", ""))
            
            # Construir input con contexto si existe
            full_input = user_message
            if context:
                context_str = ", ".join([f"{k}: {v}" for k, v in context.items()])
                full_input = f"[Contexto: {context_str}]\n\n{user_message}"
            
            # Ejecutar agente
            response = agent.run(full_input)
            
            return {
                "success": True,
                "response": response,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error ejecutando agente: {e}")
            return {
                "success": False,
                "response": None,
                "error": str(e)
            }
    
    @classmethod
    def clear_memory(cls):
        """Limpia la memoria conversacional"""
        if cls._memory:
            cls._memory.clear()
            logger.info("Memoria conversacional limpiada")
