from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router
from app.database import Base, engine
from app.config import settings

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartEat AI API",
    description="Backend API for SmartEat AI - Personalized meal planning and nutrition tracking",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Allow frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Register routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])