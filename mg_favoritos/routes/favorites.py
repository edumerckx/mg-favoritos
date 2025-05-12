from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session as SessionORM

from mg_favoritos.database import get_session
from mg_favoritos.models import Customer, Favorite
from mg_favoritos.schemas.favorites import (
    FavoriteList,
    FavoriteResponse,
    FavoriteSchema,
)
from mg_favoritos.security import get_customer
from mg_favoritos.services.products import get_product, get_products

router = APIRouter(prefix='/favorites', tags=['favorites'])
Session = Annotated[SessionORM, Depends(get_session)]
CurrentCustomer = Annotated[Customer, Depends(get_customer)]


@router.get('/', status_code=HTTPStatus.OK, response_model=FavoriteList)
async def get_favorites(session: Session, current_customer: CurrentCustomer):
    """
    Busca os favoritos do usuário logado
    """
    favorites = await session.scalars(
        select(Favorite).where(Favorite.customer_id == current_customer.id)
    )
    favorites = favorites.all()

    products = []

    if len(favorites) > 0:
        products = await get_products(favorites)

    return {'favorites': products}


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=FavoriteResponse,
)
async def create_favorite(
    favorite: FavoriteSchema,
    session: Session,
    current_customer: CurrentCustomer,
):
    """
    Adiciona um favorito ao usuário logado

    - `favorite`: FavoriteSchema
    """
    db_favorite = await session.scalar(
        select(Favorite).where(
            Favorite.customer_id == current_customer.id,
            Favorite.product_id == favorite.product_id,
        )
    )
    if db_favorite:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Favorite already exists'
        )
    product_exists = await get_product(favorite.product_id)
    if not product_exists:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    favorite = Favorite(
        customer_id=current_customer.id,
        product_id=favorite.product_id,
    )
    session.add(favorite)
    await session.commit()
    await session.refresh(favorite)
    return favorite


@router.delete('/{id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_favorite(
    id: int, session: Session, current_customer: CurrentCustomer
):
    """
    Deleta um favorito pelo ID

    - `id`: int - id do produto favoritado
    """
    db_favorite = await session.scalar(
        select(Favorite).where(
            Favorite.customer_id == current_customer.id,
            Favorite.product_id == id,
        )
    )
    if not db_favorite:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Favorite not found'
        )

    await session.delete(db_favorite)
    await session.commit()
