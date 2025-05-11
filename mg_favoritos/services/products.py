from httpx import AsyncClient

from mg_favoritos.models import Favorite
from mg_favoritos.schemas.products import ProductResponse
from mg_favoritos.settings import Settings


async def get_products(favorites: list[Favorite]) -> list[ProductResponse]:
    async with AsyncClient() as client:
        products = []
        for favorite in favorites:
            response = await client.get(
                f'{Settings().PRODUCTS_ENDPOINT}/{favorite.product_id}'
            )
            try:
                data = response.json()
                if data:
                    favorite_response = ProductResponse(
                        product_id=favorite.product_id,
                        title=data.get('title'),
                        image_url=data.get('image'),
                        price=data.get('price'),
                        review=data.get('rating', {}).get('rate'),
                    )
                    products.append(favorite_response)
            except Exception:
                continue

        return products


async def get_product(product_id: int) -> bool:
    async with AsyncClient() as client:
        response = await client.get(
            f'{Settings().PRODUCTS_ENDPOINT}/{product_id}'
        )

        try:
            data = response.json()
            if data:
                return True
            return False
        except Exception:
            return False
