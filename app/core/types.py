import enum


class OrderStatus(enum.Enum):
    """Состояние заказа"""
    PROCESSING = 'обработка'
    SENT = 'отправлен'
    DELIVERED = 'доставлен'


class DBType(enum.StrEnum):
    """Тип используемой БД"""
    POSTGRESQL = 'pg'
    SQLITE = 'sqlite'
