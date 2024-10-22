from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.types import OrderStatus
from app.core.constants import MAX_PRODUCT_NAME_LENGTH


class Base(DeclarativeBase):
    """База для отображённых (mapped) классов."""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Product(Base):
    """Товар (mapped class)."""
    __tablename__ = 'product'

    name: Mapped[str] = mapped_column(String(MAX_PRODUCT_NAME_LENGTH))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[int]
    amount: Mapped[int]


class Order(Base):
    """Заказ (mapped class)."""
    __tablename__ = 'order'

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )
    status: Mapped[OrderStatus]
    items: Mapped[list['OrderItem']] = relationship(lazy='joined')


class OrderItem(Base):
    """Позиция заказа (mapped class)."""
    __tablename__ = 'order_item'

    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='restrict')
    )
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    amount: Mapped[int]
