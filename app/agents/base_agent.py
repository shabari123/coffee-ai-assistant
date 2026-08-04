from abc import ABC, abstractmethod

from app.services.gemini_service import GeminiService
from app.models.agent_context import AgentContext


class BaseAgent(ABC):

    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    @abstractmethod
    def chat(self, context: AgentContext) -> str:
        pass