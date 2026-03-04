from app.database import SessionLocal
from app.services.profile import ProfileService
from app.schemas.profile import ProfileResponse

from langchain.tools import tool

@tool
def get_user_profile_summary(user_id: int):
    """
    Gets the complete user profile: personal data, health goals, tastes, and dietary restrictions.
    
    WHEN TO USE:
    - When the user greets or starts a conversation (to personalize the response)
    - When they ask about their data, profile, preferences, or restrictions
    - When they say: "my data", "my profile", "what do you know about me", "my preferences"
    
    WHEN NOT TO USE:
    - To view the nutritional plan (use get_current_plan_summary)
    - To search for recipes (use search_recipes_by_criteria)
    
    Returns: profile data without the user's name.
    """
    db = SessionLocal()
    try:
        profile = ProfileService.get_user_profile(db, user_id=user_id)
        
        if not profile:
            return {
                "result": "No profile found for this user",
                "profile": None
            }
        
        # Convert to dictionary to make it serializable
        # mode='json' ensures date/datetime is serialized as ISO string
        profile_data = ProfileResponse.model_validate(profile).model_dump(mode='json')
        
        return {
            "result": "Profile found",
            "profile": profile_data,
        }
        
    except Exception as e:
        return {
            "result": f"Error getting profile: {str(e)}",
            "profile": None
        }
    finally:
        db.close()