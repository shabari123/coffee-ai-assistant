from app.agents.product_agent import ProductAgent
from app.agents.knowledge_agent import KnowledgeAgent
from app.agents.order_agent import OrderAgent
from app.models.agent_context import AgentContext
from app.models.chat_message import ChatMessage
from app.services.gemini_service import GeminiService
from app.agents.recommendation_agent import RecommendationAgent
import logging

logger = logging.getLogger(__name__)

class RouterAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.product_agent = ProductAgent(gemini_service)
        self.knowledge_agent = KnowledgeAgent(gemini_service)
        self.order_agent = OrderAgent(gemini_service)
        self.recommendation_agent = RecommendationAgent(gemini_service)

        self.agents = {
            "ProductAgent": self.product_agent,
            "KnowledgeAgent": self.knowledge_agent,
            "OrderAgent": self.order_agent,
            "RecommendationAgent": self.recommendation_agent,
        }

    def chat(self, message: str, context: AgentContext):
        agent_name = self.route(message)
        logger.info("Routing -> %s", agent_name)
        agent = self.agents.get(agent_name)

        if not agent:
            return "I couldn't determine which agent should handle your request."

        return agent.chat(context)


    def route(self, message: str) -> str:
        prompt = f"""
        You are an AI router.

        Your job is to select exactly one agent.

        Available agents:

        ProductAgent
        - Product information
        - Product search
        - Product pricing

        RecommendationAgent
        - Coffee recommendations
        - Help me choose a coffee
        - Suggest a coffee
        - Which coffee should I buy?
        - Recommend the best coffee

        KnowledgeAgent
        - Coffee education
        - Brewing guides
        - Blogs
        - Refund policy
        - Shipping policy
        - FAQs

        OrderAgent
        - Order status
        - Order tracking
        - Order cancellation

        Return ONLY one of:

        ProductAgent
        KnowledgeAgent
        OrderAgent
        RecommendationAgent

        User:

        {message}
        """

        response = self.gemini_service.generate_text(
            prompt=prompt
        )

        return response.strip()