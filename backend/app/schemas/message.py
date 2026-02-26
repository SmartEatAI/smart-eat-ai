from datetime import datetime
from typing import List, Union, Optional
from pydantic import BaseModel, Field
from enums import MessageRoleEnum
from app.schemas.recipe import RecipeResponse


class MessageBase(BaseModel):
    role: MessageRoleEnum = Field(..., description="Role of the message sender (user or chef)")
    content: str = Field(..., description="Content of the message")
    timestamp: datetime = Field(..., description="When the message was sent")


class MessageSuggestion(MessageBase):
    original_recipe: RecipeResponse = Field(..., description="Original recipe")
    suggested_recipe: RecipeResponse = Field(..., description="Recipe suggested by chef")
    accepted: bool = Field(False, description="Indicates if the user accepted the suggestion")


class Chat(BaseModel):
    message: MessageBase | MessageSuggestion = Field(..., description="The latest message in the chat")
    history: Optional[List[Union[MessageBase, MessageSuggestion]]] = Field(
        None, description="Chat history between user and chef"
    )