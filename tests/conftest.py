import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

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


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        poolclass=StaticPool,
        connect_args={'check_same_thread': False},
    )

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def customer(session):
    password = '123456'
    customer = Customer(
        name='Teste',
        email='test@example.com',
        password=get_hash(password),
    )
    session.add(customer)
    await session.commit()
    await session.refresh(customer)

    customer.raw_password = password  # usado somente para testes!
    return customer


@pytest_asyncio.fixture
async def favorite(session, customer):
    favorite = Favorite(
        customer_id=customer.id,
        product_id=1,
    )
    session.add(favorite)
    await session.commit()
    await session.refresh(favorite)  # usado somente para testes!
    return favorite


@pytest.fixture
def token(client, customer):
    resp = client.post(
        '/auth/token',
        data={'username': customer.email, 'password': customer.raw_password},
    )
    return resp.json()['access_token']
