from app.agents.base_agent import BaseAgent
from app.models.agent_context import AgentContext
from app.models.agent_response import AgentResponse
from app.registry.tool_registry import ToolRegistry


class ProductAgent(BaseAgent):

    def chat(self, context: AgentContext) -> AgentResponse:

        result = self.gemini_service.generate_chat(
            messages=context.messages,
            tools=ToolRegistry.product_tools(),
        )

        products = []

        # Extract products returned by tools
        for tool_result in result.tool_results:

            if isinstance(tool_result, dict):

                result_data = tool_result.get("result", [])

                if isinstance(result_data, list):
                    products.extend(result_data)

                elif isinstance(result_data, dict):
                    products.append(result_data)

        # Remove duplicate products by ID
        unique_products = {}

        for product in products:

            # Product is a Pydantic Product object
            if hasattr(product, "id"):
                unique_products[product.id] = product

            # Keep support for dictionaries as well
            elif isinstance(product, dict) and "id" in product:
                unique_products[product["id"]] = product

        products = list(unique_products.values())

        return AgentResponse(
            response=result.text,
            products=products,
        )