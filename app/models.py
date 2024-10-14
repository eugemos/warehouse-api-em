from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.types import OrderStatus


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Product(Base):
    __tablename__ = 'product'

    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[int]
    amount: Mapped[int]


class Order(Base):
    __tablename__ = 'order'

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )
    status: Mapped[OrderStatus]


class OrderItem(Base):
    __tablename__ = 'order_item'

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    amount: Mapped[int]
