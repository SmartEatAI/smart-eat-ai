import random
from app.models.recipe import Recipe
from app.models.user import User
from app.models.plan import Plan
from app.schemas.recipe import RecipeResponse
from sqlalchemy.orm import Session
from app.core.ml_model import ml_model

def get_meal_order(n_meals: int):
    mapping = {
        3: ["breakfast", "lunch", "dinner"],
        4: ["breakfast", "lunch", "snack", "dinner"],
        5: ["breakfast", "snack", "lunch", "snack", "dinner"],
        6: ["breakfast", "snack", "lunch", "snack", "dinner", "snack"]
    }
    return mapping.get(n_meals, mapping[3])

def swap_for_similar(
    db: Session,
    user: User,
    recipe_id: int,
    meal_label: str,
    n_search: int = 550,
):
    profile = user.profile
    if profile is None:
        return None

    plan = (
        db.query(Plan)
        .filter(Plan.user_id == user.id, Plan.active.is_(True))
        .first()
    )

    exclude_ids = (
        {
            meal.recipe_id
            for day in plan.daily_menus
            for meal in day.meal_details
        }
        if plan
        else set()
    )

    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        return None

    df_recipes = ml_model.df
    knn = ml_model.knn
    X_scaled_all = ml_model.X_scaled_all

    required_diets = {d.name.lower() for d in profile.diet_types}

    idx_list = df_recipes.index[
        df_recipes["recipe_id"] == recipe_id
    ].tolist()

    if not idx_list:
        return None

    base_index = idx_list[0]
    recipe_vec = X_scaled_all[base_index].reshape(1, -1)

    distances, indices = knn.kneighbors(
        recipe_vec, n_neighbors=n_search
    )

    valid_neighbors = []

    for pos, idx in enumerate(indices[0][1:], start=1):

        candidate_id = int(df_recipes.iloc[idx]["recipe_id"])

        if candidate_id in exclude_ids:
            continue

        neighbor = (
            db.query(Recipe)
            .filter(Recipe.id == candidate_id)
            .first()
        )

        if not neighbor:
            continue

        recipe_meals = {m.name.lower() for m in neighbor.meal_types}
        recipe_diets = {d.name.lower() for d in neighbor.diet_types}

        if meal_label.lower() not in recipe_meals:
            continue

        if not required_diets.issubset(recipe_diets):
            continue

        response = RecipeResponse.model_validate(neighbor).model_dump()
        response["assigned_meal_type"] = meal_label
        response["distance"] = float(distances[0][pos])

        valid_neighbors.append(response)

    if not valid_neighbors:
        return None

    if len(valid_neighbors) == 1:
        return valid_neighbors[0]

    return random.choice(valid_neighbors)