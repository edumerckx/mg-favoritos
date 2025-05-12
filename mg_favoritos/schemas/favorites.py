from pydantic import BaseModel

from mg_favoritos.schemas.products import ProductResponse


class FavoriteSchema(BaseModel):
    product_id: int


class FavoriteResponse(BaseModel):
    id: int
    customer_id: int
    product_id: int


class FavoriteList(BaseModel):
    favorites: list[ProductResponse]
