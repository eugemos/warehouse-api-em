import enum


class OrderStatus(enum.Enum):
    PROCESSING = 'обработка'
    SENT = 'отправлен'
    DELIVERED = 'доставлен'
