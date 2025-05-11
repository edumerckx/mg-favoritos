from http import HTTPStatus
from sqlite3 import IntegrityError
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session as SessionORM

from mg_favoritos.database import get_session
from mg_favoritos.models import Customer
from mg_favoritos.schemas.customer import CustomerResponse, CustomerSchema
from mg_favoritos.security import get_customer, get_hash

router = APIRouter(tags=['customers'], prefix='/customers')

Session = Annotated[SessionORM, Depends(get_session)]
CurrentCustomer = Annotated[Customer, Depends(get_customer)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=CustomerResponse
)
def create_customer(customer: CustomerSchema, session: Session):
    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        password=get_hash(customer.password),
    )

    try:
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
        return new_customer
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=CustomerResponse)
def get_customer(id: int, session: Session, current_customer: CurrentCustomer):
    if current_customer.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    customer = session.scalar(select(Customer).where(Customer.id == id))
    if not customer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Customer not found'
        )
    return customer


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=CustomerResponse)
def update_customer(
    id: int,
    customer: CustomerSchema,
    session: Session,
    current_customer: CurrentCustomer,
):
    if current_customer.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_customer.name = customer.name
        current_customer.email = customer.email
        current_customer.password = get_hash(customer.password)

        session.commit()
        session.refresh(current_customer)
        return current_customer
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Email already exists'
        )


@router.delete('/{id}', status_code=HTTPStatus.NO_CONTENT)
def delete_customer(
    id: int, session: Session, current_customer: CurrentCustomer
):
    if current_customer.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_customer)
    session.commit()
