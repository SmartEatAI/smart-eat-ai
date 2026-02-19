from pydantic import BaseModel

# Esquemas para Restricciones
class RestrictionBase(BaseModel):
    name: str

class RestrictionResponse(RestrictionBase):
    id: int
    class Config:
        from_attributes = True