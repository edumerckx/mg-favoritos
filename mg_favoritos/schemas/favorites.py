from pydantic import BaseModel

from mg_favoritos.schemas.products import ProductResponse


class FavoriteSchema(BaseModel):
    customer_id: int
    product_id: int


class FavoriteResponse(FavoriteSchema):
    id: int


class FavoriteList(BaseModel):
    favorites: list[ProductResponse]
