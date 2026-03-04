from app.database import SessionLocal
from app.models.user import User
from app.models.taste import Taste
from app.models.restriction import Restriction
from app.crud.category import get_or_create_category

from langchain.tools import tool

@tool
def update_user_preference(user_id: int, preference_type: str, category_name: str):
    """
    Adds tastes, preferences, restrictions, intolerances, or allergies to the user's profile.
    
    WHEN TO USE:
    - "I don't like fish" → preference_type="restriction", category_name="fish"
    - "I'm allergic to nuts" → preference_type="restriction", category_name="nuts"
    - "I love chicken" → preference_type="taste", category_name="chicken"
    - "I'm lactose intolerant" → preference_type="restriction", category_name="lactose"
    - "I prefer Mediterranean food" → preference_type="taste", category_name="Mediterranean"
    
    WHEN NOT TO USE:
    - To view the profile (use get_user_profile_summary)
    - To modify the plan (use suggest_recipe_alternatives + replace_meal_in_plan)
    
    PARAMETERS:
    - preference_type: "taste" (positive likes) or "restriction" (allergies, intolerances, dislikes)
    - category_name: the food, ingredient, or culinary style mentioned
    
    This information is automatically used in future searches and plan generation.
    """
    db = SessionLocal()
    try:
        if preference_type not in ['taste', 'restriction']:
            return {"result": "Error: preference_type must be 'taste' or 'restriction'."}
        
        # Find or create category with the correct model
        model = Taste if preference_type == 'taste' else Restriction
        category = get_or_create_category(db, model, category_name)
        
        # Add to profile
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return {"result": "User or profile not found", "profile": None}
        
        profile = user.profile
        
        if preference_type == 'taste':
            if category not in profile.tastes:
                profile.tastes.append(category)
            result_msg = f"👍 Taste '{category_name}' added to your profile"
        else:
            if category not in profile.restrictions:
                profile.restrictions.append(category)
            result_msg = f"⚠️ Restriction '{category_name}' added to your profile"
        
        db.commit()
        
        # Recalculate macros if necessary (in case the restriction affects)
        if preference_type == 'restriction':
            # You might want to regenerate the plan if there is an active plan
            pass
        
        from app.schemas.profile import ProfileResponse
        # mode='json' ensures date/datetime is serialized as ISO string
        profile_response = ProfileResponse.model_validate(profile).model_dump(mode='json')
        
        return {
            "result": result_msg,
            "profile": profile_response
        }
    except Exception as e:
        db.rollback()
        return {"result": f"Error updating preferences: {str(e)}", "profile": None}
    finally:
        db.close()