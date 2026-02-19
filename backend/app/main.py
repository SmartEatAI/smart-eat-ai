from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth
from app.config import settings
from app.database import engine, Base

# Create database tables - solo si se gestiona la db con sqlalchemy, si se usa alembic no es necesario
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartEat AI API",
    description="Backend API for SmartEat AI - Personalized meal planning and nutrition tracking",
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

# Include routers
app.include_router(auth.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "SmartEat AI API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}