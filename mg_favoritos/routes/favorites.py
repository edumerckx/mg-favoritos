from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session as SessionORM

from mg_favoritos.database import get_session
from mg_favoritos.models import Customer, Favorite
from mg_favoritos.schemas.favorites import FavoriteList, FavoriteResponse
from mg_favoritos.security import get_customer
from mg_favoritos.services.products import get_product, get_products

router = APIRouter(prefix='/favorites', tags=['favorites'])
Session = Annotated[SessionORM, Depends(get_session)]
CurrentCustomer = Annotated[Customer, Depends(get_customer)]


@router.get('/', status_code=HTTPStatus.OK, response_model=FavoriteList)
async def get_favorites(session: Session, current_customer: CurrentCustomer):
    favorites = session.scalars(
        select(Favorite).where(Favorite.customer_id == current_customer.id)
    ).all()

    products = []

    if len(favorites) > 0:
        products = await get_products(favorites)

    return {'favorites': products}


@router.post(
    '/{product_id}',
    status_code=HTTPStatus.CREATED,
    response_model=FavoriteResponse,
)
async def create_favorite(
    product_id: int,
    session: Session,
    current_customer: CurrentCustomer,
):
    product_exists = await get_product(product_id)
    if not product_exists:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    db_favorite = session.scalar(
        select(Favorite).where(
            Favorite.customer_id == current_customer.id,
            Favorite.product_id == product_id,
        )
    )
    if db_favorite:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Favorite already exists'
        )

    favorite = Favorite(
        customer_id=current_customer.id,
        product_id=product_id,
    )
    session.add(favorite)
    session.commit()
    session.refresh(favorite)
    return favorite
