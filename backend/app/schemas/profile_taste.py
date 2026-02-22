from pydantic import BaseModel, Field

# Esquema base para ProfileTaste
class ProfileTasteBase(BaseModel):
    profile_id: int = Field(..., description="Profile ID")
    taste_id: int = Field(..., description="Taste ID")

# Esquema para la respuesta de ProfileTaste
class ProfileTasteResponse(ProfileTasteBase):
    class Config:
        from_attributes = True