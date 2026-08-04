from app.tools.product_tool import (get_products, search_products,
                                    get_order_status, get_product)
from app.tools.knowledge_tool import search_knowledge

class ToolRegistry:
    @staticmethod
    def product_tools() -> list:
        return [
            get_products,
            search_products,
            get_product,
        ]

    @staticmethod
    def knowledge_tools() -> list:
        return [
            search_knowledge,
        ]

    @staticmethod
    def order_tools() -> list:
        return [
            get_order_status,
        ]

    @staticmethod
    def recommendation_tools() -> list:
        return [
            get_products,
            search_products,
            get_product,
            search_knowledge,
        ]