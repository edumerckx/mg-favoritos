from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session as SessionORM

from mg_favoritos.database import get_session
from mg_favoritos.models import Client
from mg_favoritos.schemas.auth import Token
from mg_favoritos.security import (
    create_token,
    get_client,
    verify,
)

router = APIRouter(prefix='/auth', tags=['auth'])

Session = Annotated[SessionORM, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token, status_code=HTTPStatus.CREATED)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    client = session.scalar(
        select(Client).where(Client.email == form_data.username)
    )

    bad_request = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail='Invalid credentials'
    )

    if not client:
        raise bad_request

    if not verify(form_data.password, client.password):
        raise bad_request

    access_token = create_token(data={'sub': client.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token, status_code=HTTPStatus.OK)
def refresh_access_token(client: Client = Depends(get_client)):
    access_token = create_token(data={'sub': client.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
