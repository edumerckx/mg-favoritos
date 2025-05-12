import pytest
from httpx import AsyncClient, Response

from mg_favoritos.models import Favorite
from mg_favoritos.schemas.products import ProductResponse
from mg_favoritos.services.products import get_product, get_products
from mg_favoritos.settings import Settings


@pytest.mark.asyncio
async def test_get_products(respx_mock):
    async with AsyncClient():
        mock_data = {
            'id': 1,
            'title': 'Product 1',
            'image': 'https://example.com/image1.jpg',
            'price': 9.99,
            'rating': {'rate': 4.5},
        }
        respx_mock.get(f'{Settings().PRODUCTS_ENDPOINT}/1').mock(
            return_value=Response(200, json=mock_data)
        )

        response = await get_products([Favorite(product_id=1, customer_id=1)])

        expected = ProductResponse(
            product_id=1,
            title='Product 1',
            image_url='https://example.com/image1.jpg',
            price=9.99,
            review=4.5,
        )
        assert len(response) == 1
        assert response[0] == expected


@pytest.mark.asyncio
async def test_get_products_with_empty_response(respx_mock):
    async with AsyncClient():
        respx_mock.get(f'{Settings().PRODUCTS_ENDPOINT}/1').mock(
            return_value=Response(200)
        )

        response = await get_products([Favorite(product_id=1, customer_id=1)])

        assert len(response) == 0


@pytest.mark.asyncio
async def test_get_product(respx_mock):
    async with AsyncClient():
        mock_data = {
            'id': 1,
            'title': 'Product 1',
            'image': 'https://example.com/image1.jpg',
            'price': 9.99,
            'rating': {'rate': 4.5},
        }
        respx_mock.get(f'{Settings().PRODUCTS_ENDPOINT}/1').mock(
            return_value=Response(200, json=mock_data)
        )

        response = await get_product(1)

        assert response


@pytest.mark.asyncio
async def test_get_product_with_empty_response(respx_mock):
    async with AsyncClient():
        respx_mock.get(f'{Settings().PRODUCTS_ENDPOINT}/1').mock(
            return_value=Response(200)
        )

        response = await get_product(1)

        assert not response
