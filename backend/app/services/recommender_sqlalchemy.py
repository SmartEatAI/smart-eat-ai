from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.models.diet_type import DietType
from app.models.meal_type import MealType
from app.core.ml_model import ml_model
from app.core.recommender import FEATURES, MACRO_WEIGHTS, normalize_label, safe_to_list
import numpy as np
import pandas as pd

# Example: Query recipes from DB and convert to DataFrame for ML

def get_recipes_df(db: Session):
    recipes = db.query(Recipe).all()
    rows = []
    for r in recipes:
        rows.append({
            "id": r.id,
            "name": r.name,
            "calories": r.calories,
            "fat_content": r.fat,
            "carbohydrate_content": r.carbs,
            "protein_content": r.protein,
            "diet_type": [dt.name for dt in r.diet_types],
            "meal_type": [mt.name for mt in r.meal_types],
            "images": r.image_url,
            # Add other fields as needed
        })
    return pd.DataFrame(rows)

# Example: Use this DataFrame in recommender logic

def recommend_recipes_sqlalchemy(db: Session, macros_obj, diets, n_meals, used_ids=None):
    if used_ids is None:
        used_ids = set()
    df_recipes = get_recipes_df(db)
    scaler = ml_model.scaler
    X_scaled_all = scaler.transform(df_recipes[FEATURES])
    meal_order = ["breakfast", "lunch", "dinner"][:n_meals]  # Adapt as needed
    final_recipes = []
    current_used_ids = used_ids.copy()
    user_diet_set = set(normalize_label(d) for d in diets)
    user_vec = np.array([[macros_obj["calories"], macros_obj["fat_content"], macros_obj["carbohydrate_content"], macros_obj["protein_content"]]])
    user_scaled = scaler.transform(user_vec) * MACRO_WEIGHTS
    for meal_label in meal_order:
        def check_diet(recipe_diets):
            r_diets = set(normalize_label(d) for d in safe_to_list(recipe_diets))
            return user_diet_set.issubset(r_diets)
        def check_meal(recipe_meals):
            r_meals = [m.lower().strip() for m in safe_to_list(recipe_meals)]
            return meal_label.lower() in r_meals
        mask_diet = df_recipes["diet_type"].apply(check_diet)
        mask_meal = df_recipes["meal_type"].apply(check_meal)
        mask_combined = mask_diet & mask_meal
        valid_indices = np.where(mask_combined)[0]
        if len(valid_indices) == 0:
            continue
        df_search = df_recipes.iloc[valid_indices].copy()
        df_search = df_search[~df_search["id"].isin(current_used_ids)]
        if df_search.empty:
            continue
        X_search = X_scaled_all[df_search.index] * MACRO_WEIGHTS
        distances = np.linalg.norm(X_search - user_scaled, axis=1)
        df_search["dist"] = distances
        best_recipe = df_search.sort_values("dist").iloc[0].to_dict()
        best_recipe["assigned_meal_type"] = meal_label
        final_recipes.append(best_recipe)
        current_used_ids.add(best_recipe["id"])
    return pd.DataFrame(final_recipes)
