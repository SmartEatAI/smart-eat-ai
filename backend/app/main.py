from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, chat, plans
from app.config import settings
from app.services.knn_service import KNNService
from app.services.langchain_agent import LangChainAgentService
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SmartEat AI API",
    description="Backend API for SmartEat AI - Personalized meal planning and nutrition tracking with LangChain",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize ML models and services on application startup
    """
    logger.info("🚀 Iniciando SmartEat AI Backend...")
    
    # Initialize KNN Model
    try:
        if os.path.exists(settings.KNN_MODEL_PATH):
            scaler_path = settings.KNN_SCALER_PATH if os.path.exists(settings.KNN_SCALER_PATH) else None
            KNNService.load_model(
                model_path=settings.KNN_MODEL_PATH,
                scaler_path=scaler_path,
                feature_columns=settings.KNN_FEATURE_COLUMNS
            )
            logger.info("✅ Modelo KNN cargado exitosamente")
        else:
            logger.warning(f"⚠️  Modelo KNN no encontrado en {settings.KNN_MODEL_PATH}")
    except Exception as e:
        logger.error(f"❌ Error cargando modelo KNN: {e}")
    
    # Initialize LangChain Agent
    try:
        LangChainAgentService.initialize(
            ollama_base_url=settings.OLLAMA_BASE_URL,
            model_name=settings.OLLAMA_MODEL,
            temperature=settings.OLLAMA_TEMPERATURE
        )
        logger.info("✅ LangChain Agent inicializado")
    except Exception as e:
        logger.error(f"❌ Error inicializando LangChain Agent: {e}")
        logger.warning("⚠️  El agente conversacional no estará disponible")
    
    logger.info("✨ Backend inicializado correctamente")


# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(plans.router, prefix="/api", tags=["Plans"])


@app.get("/")
def root():
    return {
        "message": "SmartEat AI API",
        "version": "1.0.0",
        "features": ["Authentication", "Chat with LangChain", "Meal Planning", "KNN Recommendations"]
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint with service status
    """
    return {
        "status": "healthy",
        "knn_loaded": KNNService.is_loaded(),
        "langchain_initialized": LangChainAgentService.is_initialized()
    }