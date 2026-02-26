from pydantic import BaseModel
from typing import Optional, List, Union


class Message(BaseModel):
    role: str
    content: str
    
class Suggestion(BaseModel):
    meal_detail_id: int
    recipe_id: int
    status: bool


class ChatPayload(BaseModel):
    message: str
    history: List[Union[Message, Suggestion]] = []

class AgentResponse(BaseModel):
    text: str
    suggestion: Optional[Suggestion] = None
    
