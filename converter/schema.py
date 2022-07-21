from datetime import datetime
from typing import List, Optional

from pydantic import Field

from db.schema import BaseSchema


class HistorySchema(BaseSchema):
    from_currency: str
    to_currency: str
    user_id: int


class GetHistorySchema(BaseSchema):
    """
    Request body for parsing calls to get history
    """
    from_currency: Optional[str]
    to_currency: Optional[str]


class CurrencySchema(BaseSchema):
    code: str
    name: str


class CurrencyListSchema(BaseSchema):
    currencies: List[CurrencySchema]


class ConvertSchema(BaseSchema):
    """
    Parses body for requests to convert currencies
    """
    from_currency: str
    to_currency: str
    amount: float = Field(gt=0, description="The amount must be greater than zero")


class ConversionResponseSchema(BaseSchema):
    """
    Schema for results of conversions
    """
    from_currency: str
    to_currency: str
    amount: float
    rate: float
    result: float


class ConversionHistoryResponseSchema(ConversionResponseSchema):
    timestamp: datetime
