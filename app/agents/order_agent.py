from app.agents.base_agent import BaseAgent
from app.models.agent_context import AgentContext
from app.models.chat_message import ChatMessage
from app.registry.tool_registry import ToolRegistry


class OrderAgent(BaseAgent):

    def chat(self, context: AgentContext) -> str:

        prompt = """
You are Swasthya Coffee's order support assistant.

You help customers with:

- Checking order status
- Tracking orders

Rules:

1. If the customer has not provided an order number,
   ask politely for it.

2. Once an order number is available,
   use the order tool.

3. Never guess an order status.

4. Only use information returned by the order tool.

5. If the tool says the order was not found,
   politely ask the customer to verify the order number.

Keep responses friendly and concise.
"""

        messages = context.messages.copy()
        messages.append(
            ChatMessage(
                role="user",
                content=prompt,
            )
        )

        return self.gemini_service.generate_chat(
            messages=messages,
            tools=ToolRegistry.order_tools(),
        )