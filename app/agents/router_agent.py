from app.agents.product_agent import ProductAgent
from app.agents.knowledge_agent import KnowledgeAgent
from app.agents.order_agent import OrderAgent
from app.models.agent_context import AgentContext
from app.models.chat_message import ChatMessage
from app.services.gemini_service import GeminiService
from app.agents.recommendation_agent import RecommendationAgent
from app.models.agent_response import AgentResponse
from app.services.preference_service import PreferenceService
from app.services.workflow_service import WorkflowService
from app.exceptions.llm_exception import LLMException
import logging

logger = logging.getLogger(__name__)

class RouterAgent:

    def __init__(
        self,
        gemini_service: GeminiService,
        preference_service: PreferenceService,
        workflow_service: WorkflowService,
    ):
        self.gemini_service = gemini_service

        self.product_agent = ProductAgent(gemini_service)
        self.knowledge_agent = KnowledgeAgent(gemini_service)
        self.order_agent = OrderAgent(gemini_service)

        self.recommendation_agent = RecommendationAgent(
            gemini_service=gemini_service,
            preference_service=preference_service,
            workflow_service=workflow_service,
        )

        self.agents = {
            "ProductAgent": self.product_agent,
            "KnowledgeAgent": self.knowledge_agent,
            "OrderAgent": self.order_agent,
            "RecommendationAgent": self.recommendation_agent,
        }

    def chat(self, message: str, context: AgentContext, agent_name: str | None = None,) -> AgentResponse:
        if agent_name is None:
            agent_name = self.route(message)

        logger.info("Routing -> %s", agent_name)

        agent = self.agents.get(agent_name)

        if not agent:
            return AgentResponse(
                response="I couldn't determine which agent should handle your request.",
                products=[],
            )

        return agent.chat(context)



    def route(self, message: str) -> str:
        prompt = f"""
    You are an AI router for Swasthya Coffee.

    Select exactly ONE agent for the user's request.

    Available agents:

    ProductAgent:
    - Product information
    - Product search
    - Product pricing
    - Product details

    RecommendationAgent:
    - Coffee recommendations
    - Help choosing a coffee
    - Suggest a coffee
    - Which coffee should I buy?
    - Recommend a coffee

    KnowledgeAgent:
    - Coffee education
    - Brewing guides
    - Coffee origins
    - Blogs
    - FAQs
    - Shipping policy
    - Refund policy

    OrderAgent:
    - Order status
    - Order tracking
    - Order cancellation

    IMPORTANT:
    Return ONLY the agent name.
    Do not return explanations.
    Do not return punctuation.
    Do not return markdown.

    Valid outputs:
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

        agent_name = response.strip()

        valid_agents = {
            "ProductAgent",
            "KnowledgeAgent",
            "OrderAgent",
            "RecommendationAgent",
        }

        if agent_name not in valid_agents:
            raise LLMException(
                f"Invalid router response: {agent_name}"
            )

        return agent_name