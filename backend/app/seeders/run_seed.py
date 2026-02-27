from app.database import SessionLocal
from app.seeders.users import seed_users
from app.seeders.categories import seed_categories
from app.seeders.profiles import seed_profiles
from app.seeders.recipes import seed_recipes
from app.seeders.plans import seed_plans


def run_seeders():
    db = SessionLocal()
    try:
        # Usuarios
        seed_users(db)

        # Categorías (meal types, diet types, eating styles)
        seed_categories(db)

        # Perfiles
        seed_profiles(db)

        # Recetas
        seed_recipes(db)

        # Planes
        seed_plans(db)
        
    finally:
        db.close()


if __name__ == "__main__":
    run_seeders()
