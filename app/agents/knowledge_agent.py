from app.agents.base_agent import BaseAgent
from app.models.agent_context import AgentContext
from app.registry.tool_registry import ToolRegistry
from app.models.agent_response import AgentResponse


class KnowledgeAgent(BaseAgent):

    def chat(self, context: AgentContext) -> AgentResponse:
        result = self.gemini_service.generate_chat(
            messages=context.messages,
            tools=ToolRegistry.knowledge_tools(),
        )

        return AgentResponse(
            response=result.text,
            products=[],
        )