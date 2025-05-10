from http import HTTPStatus
from sqlite3 import IntegrityError
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session as SessionORM

from mg_favoritos.database import get_session
from mg_favoritos.models import Client
from mg_favoritos.schemas.client import ClientResponse, ClientSchema
from mg_favoritos.security import get_client, get_hash

router = APIRouter(tags=['clients'], prefix='/clients')

Session = Annotated[SessionORM, Depends(get_session)]
CurrentClient = Annotated[Client, Depends(get_client)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ClientResponse)
def create_client(client: ClientSchema, session: Session):
    new_client = Client(
        name=client.name,
        email=client.email,
        password=get_hash(client.password),
    )

    try:
        session.add(new_client)
        session.commit()
        session.refresh(new_client)
        return new_client
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=ClientResponse)
def get_client(id: int, session: Session, current_client: CurrentClient):
    if current_client.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    client = session.scalar(select(Client).where(Client.id == id))
    if not client:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Client not found'
        )
    return client


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=ClientResponse)
def update_client(
    id: int,
    client: ClientSchema,
    session: Session,
    current_client: CurrentClient,
):
    if current_client.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_client.name = client.name
        current_client.email = client.email
        current_client.password = get_hash(client.password)

        session.commit()
        session.refresh(current_client)
        return current_client
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Email already exists'
        )


@router.delete('/{id}', status_code=HTTPStatus.NO_CONTENT)
def delete_client(id: int, session: Session, current_client: CurrentClient):
    if current_client.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_client)
    session.commit()
