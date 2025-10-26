from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class MessageGenerateRequest(BaseModel):
    emotion: str
    language: str

class MessageGenerateResponse(BaseModel):
    message: str
    emotion: str
    language: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SaveMessageRequest(BaseModel):
    emotion: str
    language: str
    message: str

class SaveMessageResponse(BaseModel):
    id: str
    message: str

class SavedMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    emotion: str
    language: str
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SavedMessagesResponse(BaseModel):
    messages: list[SavedMessage]