from pydantic import BaseModel

# Esquema base para ProfileTaste
class ProfileTasteBase(BaseModel):
    profile_id: int
    taste_id: int

# Esquema para la respuesta de ProfileTaste
class ProfileTasteResponse(ProfileTasteBase):
    class Config:
        from_attributes = True