from pydantic import BaseModel


class ProductResponse(BaseModel):
    product_id: int
    title: str
    image_url: str
    price: float
    review: float | None
