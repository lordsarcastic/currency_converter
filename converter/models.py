from datetime import datetime
from typing import Type
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base


class ConversionHistory(Base):
    from_currency = Column(String(12), index=True, nullable=False)
    to_currency = Column(String(12), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    result = Column(Float, nullable=False)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User")
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow())

    @classmethod
    def to_dict(cls, instance: Type[Base]):
        result = {}

        for column in instance.__table__.columns:
            result[column.name] = str(getattr(instance, column.name))

        return result
