from woocommerce import API
from app.models.product import Product

from app.config import (WOOCOMMERCE_URL, WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET,)


class WooCommerceService:

    def __init__(self):
        self.client = API(
            url=WOOCOMMERCE_URL,
            consumer_key=WOOCOMMERCE_CONSUMER_KEY,
            consumer_secret=WOOCOMMERCE_CONSUMER_SECRET,
            version="wc/v3",
        )

    def _map_to_product(self, product_data: dict) -> Product:
        return Product(
            id=product_data["id"],
            name=product_data["name"],
            slug=product_data["slug"],
            price=float(product_data["price"]) if product_data["price"] else 0.0,
            description=product_data["short_description"],
            stock_status=product_data["stock_status"],
            category=[c["name"] for c in product_data["categories"]],
            image_url=product_data["images"][0]["src"] if product_data["images"] else None,
        )

    def get_products(self) -> list[Product]:
        response = self.client.get("products")
        if response.status_code != 200:
            raise Exception(f"Failed to fetch products: {response.status_code} - {response.text}")

        return [self._map_to_product(product) for product in response.json()]
    
    def search_products(self, keyword: str) -> list[Product]:
        response = self.client.get("products", params={"search": keyword})

        if response.status_code != 200:
            raise Exception(f"Failed to search products: {response.status_code} - {response.text}")

        return [self._map_to_product(product) for product in response.json()]
    
    def get_product(self, product_name: str) -> Product | None:
        response = self.client.get("products", params={"search": product_name})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch product {product_name}: {response.status_code} - {response.text}")
        products = [self._map_to_product(product) for product in response.json()]
        return products[0] if products else None

    def get_order(self, order_id: int) -> dict | None:
        response = self.client.get(f"orders/{order_id}")

        if response.status_code == 404:
            return None

        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch order {order_id}: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()