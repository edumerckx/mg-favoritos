from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session as SessionORM

from mg_favoritos.database import get_session
from mg_favoritos.models import Client
from mg_favoritos.settings import Settings

pwd_context = PasswordHash.recommended()
settings = Settings()
OAuth2Scheme = Annotated[
    str, Depends(OAuth2PasswordBearer(tokenUrl='auth/token'))
]
Session = Annotated[SessionORM, Depends(get_session)]


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_hash(password):
    return pwd_context.hash(password)


def create_token(data):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('America/Sao_Paulo')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    return encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_client(token: OAuth2Scheme, session: Session):
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get('sub')
    except DecodeError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token'
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Token expired'
        )

    client = session.scalar(select(Client).where(Client.email == email))
    if not client:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Unable to validate credentials',
        )

    return client
