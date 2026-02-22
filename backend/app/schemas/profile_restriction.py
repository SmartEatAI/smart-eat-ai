from pydantic import BaseModel, Field

# Esquema base para ProfileRestriction
class ProfileRestrictionBase(BaseModel):
    profile_id: int = Field(..., description="Profile ID")
    restriction_id: int = Field(..., description="Restriction ID")

# Esquema para la respuesta de ProfileRestriction
class ProfileRestrictionResponse(ProfileRestrictionBase):
    class Config:
        from_attributes = True