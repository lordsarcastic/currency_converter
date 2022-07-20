from datetime import datetime
from typing import Type

from sqlalchemy import (
    Column,
    DateTime,
    String
)

from db.base import Base


class User(Base):
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255))
    password = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow())

    @classmethod
    def to_dict(cls, instance: Type[Base]):
        result = {}

        for column in instance.__table__.columns:
            result[column.name] = str(getattr(instance, column.name))
        
        return result