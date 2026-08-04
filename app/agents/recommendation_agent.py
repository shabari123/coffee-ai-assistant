from app.agents.base_agent import BaseAgent
from app.constants.workflows import RECOMMENDATION_WORKFLOW
from app.models.agent_context import AgentContext
from app.models.chat_message import ChatMessage
from app.registry.tool_registry import ToolRegistry
from app.services.preference_service import PreferenceService
from app.services.workflow_service import WorkflowService
import logging

logger = logging.getLogger(__name__)

class RecommendationAgent(BaseAgent):
    def __init__(self, gemini_service):
        super().__init__(gemini_service)
        self.preference_service = PreferenceService()
        self.workflow_service = WorkflowService()

    def chat(self, context: AgentContext) -> str:
        preference = self.preference_service.get(context.session_id)
        logger.info("User preferences: %s", preference)

        if not preference.bean_type:
            self.workflow_service.start(context.session_id, RECOMMENDATION_WORKFLOW)
            return (
                "Before I recommend a coffee, "
                "do you prefer:\n\n"
                "• Arabica\n"
                "• Robusta\n"
                "• Blend"
            )
        if not preference.brew_method:
            self.workflow_service.start(context.session_id, RECOMMENDATION_WORKFLOW)
            return (
                "Great! How do you usually brew your coffee?\n\n"
                "• Filter Coffee\n"
                "• Espresso\n"
                "• French Press"
            )
        
        if not preference.strength:
            self.workflow_service.start(context.session_id, RECOMMENDATION_WORKFLOW)
            return (
                "What kind of coffee strength do you prefer?\n\n"
                "• Mild\n"
                "• Medium\n"
                "• Strong"
            )
        prompt = f"""
You are an expert coffee consultant for Swasthya Coffee.

Customer Preferences:

- Bean Type: {preference.bean_type}
- Brew Method: {preference.brew_method}
- Strength: {preference.strength}

You have access to two kinds of tools:

1. Product tools
   - Search products
   - Retrieve product details

2. Knowledge tool
   - Learn about coffee
   - Brewing methods
   - Bean characteristics
   - Coffee origins
   - FAQs
   - Policies

First understand the customer's preferences.

Use the tools when needed.

Recommend exactly ONE product.

Only recommend products returned by the product tool.

Do not invent product names.

Explain why this product is the best match for the customer.
"""
        
        messages = context.messages.copy()
        messages.append(ChatMessage(role="user", content=prompt))
        response = self.gemini_service.generate_chat(messages=messages, tools=ToolRegistry.recommendation_tools())
        if response:
            self.workflow_service.clear(context.session_id)
        return response