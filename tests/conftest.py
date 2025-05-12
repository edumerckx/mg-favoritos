import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from mg_favoritos.app import app
from mg_favoritos.database import get_session
from mg_favoritos.models import Customer, Favorite, table_registry
from mg_favoritos.security import get_hash


@pytest.fixture
def client(session):
    def _get_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = _get_session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        poolclass=StaticPool,
        connect_args={'check_same_thread': False},
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def customer(session):
    password = '123456'
    customer = Customer(
        name='Teste',
        email='test@example.com',
        password=get_hash(password),
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)

    customer.raw_password = password  # usado somente para testes!
    return customer


@pytest.fixture
def favorite(session, customer):
    favorite = Favorite(
        customer_id=customer.id,
        product_id=1,
    )
    session.add(favorite)
    session.commit()
    session.refresh(favorite)  # usado somente para testes!
    return favorite


@pytest.fixture
def token(client, customer):
    resp = client.post(
        '/auth/token',
        data={'username': customer.email, 'password': customer.raw_password},
    )
    return resp.json()['access_token']
