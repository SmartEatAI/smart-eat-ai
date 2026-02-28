from typing import Annotated, TypedDict, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage
import operator
from app.schemas.profile import ProfileResponse
from app.schemas.plan import PlanResponse
from pydantic import BaseModel

class DietGraphState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    profile: Optional[ProfileResponse] # Usamos el Response porque incluye los IDs de gustos/restricciones
    active_plan: Optional[PlanResponse] 