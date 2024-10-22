import enum


class OrderStatus(enum.Enum):
    """Состояние заказа"""

    PROCESSING = 'обработка'
    SENT = 'отправлен'
    DELIVERED = 'доставлен'
