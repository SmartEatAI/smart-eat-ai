from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, eating_style, meal_type, profile, restriction, taste, diet_type, recipe, meal_detail, daily_menu, plan
from app.config import settings

# Create database tables - solo si se gestiona la db con sqlalchemy, si se usa alembic no es necesario
#from app.database import engine, Base
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

# Include routers - definidos en routes/*.py
app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(restriction.router, prefix="/api")
app.include_router(eating_style.router, prefix="/api")
app.include_router(taste.router, prefix="/api")
app.include_router(meal_type.router, prefix="/api")
app.include_router(plan.router, prefix="/api")
app.include_router(recipe.router, prefix="/api")
app.include_router(daily_menu.router, prefix="/api")
app.include_router(diet_type.router, prefix="/api")
app.include_router(meal_detail.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "SmartEat AI API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}