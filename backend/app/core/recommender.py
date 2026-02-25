import numpy as np
import pandas as pd
import json
from typing import List, Optional, Set

from app.core.ml_model import ml_model


# =========================
# CONFIG
# =========================

FEATURES = ['calories', 'fat_content', 'carbohydrate_content', 'protein_content']
MACRO_WEIGHTS = np.array([1.5, 0.8, 1.0, 1.2])


# =========================
# UTILIDADES
# =========================

def safe_to_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]

    if isinstance(value, str):
        value = value.strip()
        if not value:
            return []

        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(v).strip() for v in parsed if str(v).strip()]
        except Exception:
            pass

        return [v.strip() for v in value.split(",") if v.strip()]

    return []


def normalize_label(s: str) -> str:
    if s is None:
        return ""
    return str(s).lower().replace(" ", "_").replace("-", "_").strip()


def get_meal_order(n_meals: int):
    mapping = {
        3: ["Breakfast", "Lunch", "Dinner"],
        4: ["Breakfast", "Lunch", "Snack", "Dinner"],
        5: ["Breakfast", "Snack", "Lunch", "Snack", "Dinner"],
        6: ["Breakfast", "Snack", "Lunch", "Snack", "Dinner", "Snack"]
    }
    return mapping.get(n_meals, mapping[3])


# =========================
# RECOMMENDATION CORE
# =========================


def recommend_recipes(
    macros_obj: dict,
    diets: List[str],
    n_meals: int,
    used_ids: Optional[Set[int]] = None
) -> pd.DataFrame:
    """
    Recommend recipes based on macros and diet preferences.
    TODO: Adapt this logic to query recipes from SQLAlchemy models instead of pandas DataFrame.
    """
    if used_ids is None:
        used_ids = set()

    # TODO: Replace ml_model.df with SQLAlchemy query for recipes
    df_recipes = ml_model.df
    scaler = ml_model.scaler
    X_scaled_all = ml_model.X_scaled_all

    meal_order = get_meal_order(n_meals)
    final_recipes = []
    current_used_ids = used_ids.copy()

    user_diet_set = set(normalize_label(d) for d in diets)

    # Vector usuario
    user_vec = np.array([[ 
        macros_obj["calories"],
        macros_obj["fat_content"],
        macros_obj["carbohydrate_content"],
        macros_obj["protein_content"]
    ]])

    user_scaled = scaler.transform(user_vec) * MACRO_WEIGHTS

    for meal_label in meal_order:
        # ---------- FILTROS ----------
        # TODO: Replace DataFrame apply with SQLAlchemy filtering
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

        # ---------- DISTANCIA ----------
        # TODO: Adapt to use recipe features from DB
        X_search = X_scaled_all[df_search.index] * MACRO_WEIGHTS
        distances = np.linalg.norm(X_search - user_scaled, axis=1)

        df_search["dist"] = distances

        best_recipe = df_search.sort_values("dist").iloc[0].to_dict()
        best_recipe["assigned_meal_type"] = meal_label

        final_recipes.append(best_recipe)
        current_used_ids.add(best_recipe["id"])

    return pd.DataFrame(final_recipes)


# =========================
# SWAP (KNN)
# =========================

def swap_for_similar(
    recipe_id: int,
    meal_label: str,
    recommended_diets: List[str],
    selected_extra: Optional[List[str]] = None,
    n_search: int = 50,
    exclude_ids: Optional[Set[int]] = None
):

    if exclude_ids is None:
        exclude_ids = set()

    if selected_extra is None:
        selected_extra = []

    df_recipes = ml_model.df
    knn = ml_model.knn
    X_scaled_all = ml_model.X_scaled_all

    required_diets = set(normalize_label(d) for d in recommended_diets)
    extra_diets = set(normalize_label(d) for d in selected_extra)

    idx_list = df_recipes.index[df_recipes["id"] == recipe_id].tolist()

    if not idx_list:
        return None

    recipe_vec = X_scaled_all[idx_list[0]].reshape(1, -1)

    _, indices = knn.kneighbors(recipe_vec, n_neighbors=n_search)

    valid_candidates = []

    for idx in indices[0][1:]:
        candidate = df_recipes.iloc[idx]
        rid = candidate["id"]

        if rid == recipe_id or rid in exclude_ids:
            continue

        candidate_meals = [
            m.lower().strip() for m in safe_to_list(candidate["meal_type"])
        ]

        if meal_label.lower() not in candidate_meals:
            continue

        candidate_diets = set(
            normalize_label(d) for d in safe_to_list(candidate["diet_type"])
        )

        if not required_diets.issubset(candidate_diets):
            continue

        if extra_diets:
            if candidate_diets & extra_diets:
                valid_candidates.append(candidate)
        else:
            valid_candidates.append(candidate)

    if not valid_candidates:
        return None

    chosen = valid_candidates[np.random.randint(len(valid_candidates))]
    result = chosen.to_dict()
    result["assigned_meal_type"] = meal_label

    return result