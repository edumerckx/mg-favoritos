from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SessionORM

from mg_favoritos.database import get_session
from mg_favoritos.models import Customer
from mg_favoritos.schemas.customer import CustomerResponse, CustomerSchema
from mg_favoritos.security import check_permissions, get_customer, get_hash

router = APIRouter(tags=['customers'], prefix='/customers')

Session = Annotated[SessionORM, Depends(get_session)]
CurrentCustomer = Annotated[Customer, Depends(get_customer)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=CustomerResponse
)
async def create_customer(customer: CustomerSchema, session: Session):
    """
    Cria um novo cliente

    - `customer`: CustomerSchema
    """
    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        password=get_hash(customer.password),
    )

    try:
        session.add(new_customer)
        await session.commit()
        await session.refresh(new_customer)
        return new_customer
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Email already exists',
        )


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=CustomerResponse)
async def get_customer(id: int, current_customer: CurrentCustomer):
    """
    Busca um cliente pelo ID

    Precisa estar logado

    - `id`: int - id do cliente
    """
    check_permissions(current_customer, id)
    return current_customer


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=CustomerResponse)
async def update_customer(
    id: int,
    customer: CustomerSchema,
    session: Session,
    current_customer: CurrentCustomer,
):
    """
    Atualiza um cliente pelo ID

    - `id`: int - id do cliente
    - `customer`: CustomerSchema
    """
    check_permissions(current_customer, id)

    try:
        current_customer.name = customer.name
        current_customer.email = customer.email
        current_customer.password = get_hash(customer.password)

        await session.commit()
        await session.refresh(current_customer)
        return current_customer
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists'
        )


@router.delete('/{id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_customer(
    id: int, session: Session, current_customer: CurrentCustomer
):
    """
    Deleta um cliente pelo ID

    - `id`: int - id do cliente"""
    check_permissions(current_customer, id)

    await session.delete(current_customer)
    await session.commit()
