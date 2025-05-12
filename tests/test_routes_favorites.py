from http import HTTPStatus

from httpx import Response

from mg_favoritos.settings import Settings


def test_create_favorite(client, token, respx_mock):
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

    response = client.post(
        '/favorites/',
        headers={'Authorization': f'Bearer {token}'},
        json={'product_id': 1},
    )

    expected = {
        'customer_id': 1,
        'product_id': 1,
        'id': 1,
    }
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected


def test_create_favorite_product_not_found(client, token, respx_mock):
    respx_mock.get(f'{Settings().PRODUCTS_ENDPOINT}/1').mock(
        return_value=Response(200)
    )
    response = client.post(
        '/favorites/',
        headers={'Authorization': f'Bearer {token}'},
        json={'product_id': 1},
    )

    excepted = {'detail': 'Product not found'}
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == excepted


def test_create_favorite_favorite_already_exists(client, token, favorite):
    response = client.post(
        '/favorites/',
        headers={'Authorization': f'Bearer {token}'},
        json={'product_id': favorite.product_id},
    )

    excepted = {'detail': 'Favorite already exists'}
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == excepted


def test_get_favorites(client, token, favorite, respx_mock):
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

    response = client.get(
        '/favorites/',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected = {
        'favorites': [
            {
                'product_id': 1,
                'title': 'Product 1',
                'image_url': 'https://example.com/image1.jpg',
                'price': 9.99,
                'review': 4.5,
            }
        ]
    }
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected


def test_delete_favorite(client, token, favorite):
    response = client.delete(
        f'/favorites/{favorite.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_favorite_not_found(client, token):
    response = client.delete(
        '/favorites/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    excepted = {'detail': 'Favorite not found'}
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == excepted
