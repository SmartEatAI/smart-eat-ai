from pydantic import BaseModel

# Esquema base para ProfileRestriction
class ProfileRestrictionBase(BaseModel):
    profile_id: int
    restriction_id: int

# Esquema para la respuesta de ProfileRestriction
class ProfileRestrictionResponse(ProfileRestrictionBase):
    class Config:
        from_attributes = True