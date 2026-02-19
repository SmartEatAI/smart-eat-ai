from pydantic import BaseModel

# Esquemas para Gustos
class TasteBase(BaseModel):
    name: str

class TasteResponse(TasteBase):
    id: int

    class Config:
        from_attributes = True