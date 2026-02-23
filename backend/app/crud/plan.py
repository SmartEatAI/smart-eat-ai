from sqlalchemy.orm import Session
from app.models.plan import Plan
from app.schemas.plan import PlanCreate
from app.models.meal_detail import MealDetail
from app.models.daily_menu import DailyMenu
from fastapi import HTTPException

def get_plan_by_current_user(db: Session, user_id: int):
    """Obtiene el plan activo del usuario actual."""
    try:
        return db.query(Plan).filter(Plan.user_id == user_id, Plan.active == True).first()
    except Exception as e:
        print(f"Database error when get_plan_by_current_user: {e}")
        raise HTTPException(status_code=500, detail="Database error when get_plan_by_current_user")

def deactivate_current_plan(db: Session, user_id: int):
    """Desactiva el plan activo del usuario actual."""
    try:
        db_plan = db.query(Plan).filter(Plan.user_id == user_id, Plan.active == True).first()
        if db_plan:
            db_plan.active = False
            db.commit()
    except Exception as e:
        print(f"Database error when deactivate_current_plan: {e}")
        raise HTTPException(status_code=500, detail="Database error when deactivate_current_plan")

def create_plan(db: Session, obj_in: PlanCreate, user_id: int):
    """Crea un plan con sus daily_menus y meal_details usando cascada."""

    try:
        data = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else obj_in
        # Crear plan vacio
        new_plan = Plan(
            user_id=user_id,
            # Podrías añadir aquí otros campos de obj_in si existen
        )

        # 3. Construimos los objetos anidados (DailyMenus)
        if "daily_menus" in data and data["daily_menus"]:
            for dm_data in data["daily_menus"]:
                new_menu = DailyMenu(
                    day_of_week=dm_data["day_of_week"]
                )
                
                # 4. Construimos los MealDetails dentro de cada DailyMenu
                if "meal_details" in dm_data:
                    for md_data in dm_data["meal_details"]:
                        new_meal = MealDetail(
                            recipe_id=md_data["recipe_id"],
                            schedule=md_data["schedule"],
                            status=md_data["status"],
                            meal_type=md_data["meal_type"]
                        )
                        new_menu.meal_details.append(new_meal)
                
                # Añadimos el menú al plan (SQLAlchemy se encarga del plan_id)
                new_plan.daily_menus.append(new_menu)

        # 5. Un solo commit para toda la estructura
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
        
        return new_plan
    except Exception as e:
        db.rollback()
        print(f"Database error when create_plan: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database error when create_plan"
        )
