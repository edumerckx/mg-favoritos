from http import HTTPStatus


def test_login_for_access_token(client, customer):
    response = client.post(
        '/auth/token',
        data={'username': customer.email, 'password': customer.raw_password},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_login_for_access_token_with_invalid_credentials(client):
    response = client.post(
        '/auth/token',
        data={'username': 'invalid', 'password': 'invalid'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_for_access_token_with_invalid_password(client, customer):
    response = client.post(
        '/auth/token',
        data={'username': customer.email, 'password': 'invalidpassword'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_refresh_access_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
