from pydantic import BaseModel

from app.models.chat_message import ChatMessage


class AgentContext(BaseModel):
    session_id: str
    messages: list[ChatMessage]