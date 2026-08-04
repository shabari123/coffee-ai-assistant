from app.agents.base_agent import BaseAgent
from app.models.agent_context import AgentContext
from app.registry.tool_registry import ToolRegistry


class ProductAgent(BaseAgent):
    def chat(self, context: AgentContext) -> str:
        return self.gemini_service.generate_chat(
            messages=context.messages,
            tools=ToolRegistry.product_tools(),
        )