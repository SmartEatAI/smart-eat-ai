from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, profile, restriction, taste, meal_detail, daily_menu, plan, diet_type, ml_model, chat
from app.config import settings
from app.core.ml_model import ml_model as ml_model_instance
# Create database tables - solo si se gestiona la db con sqlalchemy, si se usa alembic no es necesario
#from app.database import engine, Base
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartEat AI API",
    description="Backend API for SmartEat AI - Personalized meal planning and nutrition tracking",
    version="1.0.0"
)

# Cargar el modelo ML al iniciar la aplicación
@app.on_event("startup")
def startup_event():
    ml_model_instance.load()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - definidos en routes/*.py
app.include_router(auth.router, prefix="/api")

# Profile
app.include_router(profile.router, prefix="/api", tags=["Profile"])
app.include_router(restriction.router, prefix="/api", tags=["Profile"])
app.include_router(diet_type.router, prefix="/api", tags=["Profile"])
app.include_router(taste.router, prefix="/api", tags=["Profile"])

# Planning
app.include_router(plan.router, prefix="/api", tags=["Plan"])
app.include_router(daily_menu.router, prefix="/api", tags=["Plan"])
app.include_router(meal_detail.router, prefix="/api", tags=["Plan"])
app.include_router(ml_model.router, prefix="/api", tags=["ML Recommender"])

# Chat
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "SmartEat AI API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}