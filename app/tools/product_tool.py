from app.services.woocommerce_service import WooCommerceService

woo_service = WooCommerceService()
import logging

logger = logging.getLogger(__name__)

def get_products():
    """
    Returns all available coffee products.
    """
    return woo_service.get_products()


def search_products(keyword: str):
    """
    Search products using a keyword.
    """
    logger.info("Searching products with keyword: %s", keyword)
    return woo_service.search_products(keyword)

def get_product(product_name: str):
    """
    Returns details of a specific coffee product.
    Use this when the user asks about a particular product by name.
    """
    logger.info("Fetching product: %s", product_name)
    product = woo_service.get_product(product_name)
    if not product:
        raise Exception(f"Product with name {product_name} not found.")
    return product

def get_order_status(order_id: int):
    """
    Get the status of a specific order by its ID.
    """
    logger.info("Fetching order: %s", order_id)

    order = woo_service.get_order(order_id)

    if order is None:
        return {
            "found": False,
            "message": f"Order {order_id} was not found."
        }

    return {
        "found": True,
        "order_id": order["id"],
        "status": order["status"],
        "total": order["total"],
        "currency": order["currency"],
        "date_created": order["date_created"],
    }