from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Client:
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    favorites: Mapped[list['Favorite']] = relationship(
        init=False, back_populates='client', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Favorite:
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    product_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    client: Mapped[Client] = relationship(
        init=False, back_populates='favorites'
    )
