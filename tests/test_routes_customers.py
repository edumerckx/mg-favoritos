from http import HTTPStatus


def test_create_customer(client):
    response = client.post(
        '/customers/',
        json={
            'name': 'Test',
            'email': 'test@example.com',
            'password': 'password',
        },
    )

    expected = {
        'id': 1,
        'name': 'Test',
        'email': 'test@example.com',
    }
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected


def test_create_customer_with_existing_email(client, customer):
    response = client.post(
        '/customers/',
        json={
            'name': 'Test',
            'email': customer.email,
            'password': 'password',
        },
    )

    excepted = {'detail': 'Email already exists'}
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == excepted


def test_get_customer(client, customer, token):
    response = client.get(
        f'/customers/{customer.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    expected = {
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
    }
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected


def test_get_customer_with_invalid_token(client, customer):
    response = client.get(
        f'/customers/{customer.id}',
        headers={'Authorization': 'Bearer invalid'},
    )
    excepted = {'detail': 'Invalid token'}
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == excepted


def test_get_customer_without_permissions(client, customer, token):
    response = client.get(
        f'/customers/{customer.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )
    excepted = {'detail': 'Not enough permissions'}
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == excepted


def test_update_customer(client, customer, token):
    response = client.put(
        f'/customers/{customer.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Test',
            'email': 'update@example.com',
            'password': '123456',
        },
    )
    expected = {
        'id': customer.id,
        'name': 'Test',
        'email': 'update@example.com',
    }
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected


def test_update_customer_with_existing_email(client, customer, token):
    data = {
        'name': 'Other Customer',
        'email': 'other@example.com',
        'password': '123456',
    }
    client.post('/customers/', json=data)

    response = client.put(
        f'/customers/{customer.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Test',
            'email': data.get('email'),
            'password': '123456',
        },
    )
    excepted = {'detail': 'Email already exists'}
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == excepted


def test_delete_customer(client, customer, token):
    response = client.delete(
        f'/customers/{customer.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
