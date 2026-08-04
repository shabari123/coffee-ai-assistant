from app.agents.base_agent import BaseAgent
from app.models.chat_message import ChatMessage
from app.registry.tool_registry import ToolRegistry


class KnowledgeAgent(BaseAgent):
    def chat(self, messages: list[ChatMessage]) -> str:
        return self.gemini_service.generate_chat(
            messages=messages,
            tools=ToolRegistry.knowledge_tools(),
        )