"""
Модели базы данных SQLAlchemy
"""
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Order(Base):
    """Модель для хранения ордеров в базе данных"""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, unique=True, nullable=False, index=True)
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # buy/sell
    order_type = Column(String, nullable=False)  # market/limit
    price = Column(Float, nullable=True)
    quantity = Column(Float, nullable=False)
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Order {self.order_id}: {self.symbol} {self.side} {self.quantity} @ {self.price}>"

    def to_dict(self):
        """Преобразование объекта в словарь"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'symbol': self.symbol,
            'side': self.side,
            'order_type': self.order_type,
            'price': self.price,
            'quantity': self.quantity,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
