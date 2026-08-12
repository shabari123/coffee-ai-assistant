from pydantic import BaseModel, Field
from typing import Any


class GeminiResponse(BaseModel):
    text: str
    tool_results: list[Any] = Field(default_factory=list)