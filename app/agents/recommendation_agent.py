from app.agents.base_agent import BaseAgent
from app.constants.workflows import RECOMMENDATION_WORKFLOW
from app.models.agent_context import AgentContext
from app.models.chat_message import ChatMessage
from app.registry.tool_registry import ToolRegistry
from app.services.preference_service import PreferenceService
from app.services.workflow_service import WorkflowService
from app.models.agent_response import AgentResponse
import logging

logger = logging.getLogger(__name__)


class RecommendationAgent(BaseAgent):

    def __init__(
        self,
        gemini_service,
        preference_service: PreferenceService,
        workflow_service: WorkflowService,
    ):
        super().__init__(gemini_service)

        self.preference_service = preference_service
        self.workflow_service = workflow_service

    def chat(self, context: AgentContext) -> AgentResponse:

        preference = self.preference_service.get(
            context.session_id
        )

        logger.info("User preferences: %s", preference)

        # --------------------------------------------------
        # 1. Ask for missing preferences
        # --------------------------------------------------

        if not preference.bean_type:
            self.workflow_service.start(
                context.session_id,
                RECOMMENDATION_WORKFLOW,
            )

            return AgentResponse(
                response=(
                    "Before I recommend a coffee, "
                    "do you prefer:\n\n"
                    "• Arabica\n"
                    "• Robusta\n"
                    "• Blend"
                ),
                products=[],
            )

        if not preference.brew_method:
            self.workflow_service.start(
                context.session_id,
                RECOMMENDATION_WORKFLOW,
            )

            return AgentResponse(
                response=(
                    "Great! How do you usually brew your coffee?\n\n"
                    "• Filter Coffee\n"
                    "• Espresso\n"
                    "• French Press"
                ),
                products=[],
            )

        if not preference.strength:
            self.workflow_service.start(
                context.session_id,
                RECOMMENDATION_WORKFLOW,
            )

            return AgentResponse(
                response=(
                    "What kind of coffee strength do you prefer?\n\n"
                    "• Mild\n"
                    "• Medium\n"
                    "• Strong"
                ),
                products=[],
            )

        # --------------------------------------------------
        # 2. All preferences are available
        # --------------------------------------------------

        prompt = f"""
You are an expert coffee consultant for Swasthya Coffee.

Customer preferences:

Bean Type: {preference.bean_type}
Brew Method: {preference.brew_method}
Strength: {preference.strength}

Your task:

1. Find products that match the customer's preferences.
2. Use the available product tools.
3. Recommend exactly ONE product.
4. The recommended product MUST come from a product tool result.
5. Never invent a product.
6. Explain briefly why the selected product matches.
7. Do not list multiple products.
8. Do not include product price, URL, or stock information.
"""

        messages = context.messages.copy()

        messages.append(
            ChatMessage(
                role="user",
                content=prompt,
            )
        )

        # --------------------------------------------------
        # 3. Ask Gemini to use product tools
        # --------------------------------------------------

        result = self.gemini_service.generate_chat(
            messages=messages,
            tools=ToolRegistry.recommendation_tools(),
        )

        # --------------------------------------------------
        # 4. Extract products returned by tools
        # --------------------------------------------------

        products = []

        for tool_result in result.tool_results:

            logger.debug(
                "Recommendation tool result: %r",
                tool_result,
            )

            if isinstance(tool_result, dict):

                result_data = tool_result.get(
                    "result",
                    [],
                )

                if isinstance(result_data, list):
                    products.extend(result_data)

                elif result_data:
                    products.append(result_data)

        # --------------------------------------------------
        # 5. Remove duplicate products
        # --------------------------------------------------

        unique_products = {}

        for product in products:

            if hasattr(product, "id"):
                unique_products[product.id] = product

            elif isinstance(product, dict) and "id" in product:
                unique_products[product["id"]] = product

        products = list(unique_products.values())

        # --------------------------------------------------
        # 6. Find the product Gemini recommended
        # --------------------------------------------------

        recommended_product = []

        if result.text:

            response_text = result.text.lower()

            for product in products:

                product_base_name = (
                    product.name.split("|")[0].strip().lower()
                )

                if product_base_name in response_text:
                    recommended_product = [product]
                    break

        # --------------------------------------------------
        # 7. Finish recommendation workflow
        # --------------------------------------------------

        if result.text and recommended_product:
            self.workflow_service.clear(
                context.session_id
            )

        return AgentResponse(
            response=result.text,
            products=recommended_product,
        )