from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    slug: str
    price: float
    description: str
    stock_status: str
    category: list[str]
    image_url: Optional[str] = None