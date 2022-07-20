from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.api import get_user
from auth.exceptions import UnvalidatedCredentials
from auth.models import User
from auth.schema import UserSchema

from auth.services import UserService, reuseable_oauth
from converter.exceptions import CURRENCY_NOT_SUPPORTED
from converter.models import ConversionHistory
from db.db import get_db

from .schema import ConversionHistoryResponseSchema, ConversionResponseSchema, ConvertSchema, CurrencyListSchema, CurrencySchema, GetHistorySchema
from .services import ConverterService


router = APIRouter(
    prefix="/currencies"
)


@router.get('/list', summary="Get list of currencies supported", response_model=CurrencyListSchema)
def get_currency_list(token: str = Depends(reuseable_oauth)):
    currency_list = ConverterService.get_currency_list()
    list_of_currencies = list()
    print("list of currencies", currency_list)

    for key, value in currency_list.items():
        list_of_currencies.append(
            CurrencySchema(code=key, name=value)
        )
    
    return CurrencyListSchema(currencies=list_of_currencies)


@router.post('/convert', summary="Convert one currency to another", response_model=ConversionResponseSchema)
def convert_currency(body: ConvertSchema, db: Session = Depends(get_db), user: Optional[User] = Depends(get_user)):
    if not user:
        raise UnvalidatedCredentials

    body.from_currency = body.from_currency.lower()
    body.to_currency = body.to_currency.lower()

    for currency in (body.from_currency, body.to_currency):
        if not ConverterService.currency_is_supported(currency):
            raise CURRENCY_NOT_SUPPORTED(currency)
    
    conversion_result = ConverterService.convert(body)
    ConverterService(db).store_conversion_to_history(
        payload=conversion_result,
        user=user.id
    )

    return conversion_result

@router.get('/history', summary="Get a history of your conversions", response_model=List[ConversionHistoryResponseSchema])
def get_history(from_currency: str = None, to_currency: str = None, db: Session = Depends(get_db), user: Optional[User] = Depends(get_user)):
    if not user:
        raise UnvalidatedCredentials

    payload = GetHistorySchema(
        from_currency=from_currency,
        to_currency=to_currency
    )

    history = ConverterService(db).get_conversion_history(
        payload=payload,
        user=user
    )

    parsed_history = list(map(
        lambda item: ConversionHistoryResponseSchema(
            **ConversionHistory.to_dict(item)
        ),
        history
    ))

    return parsed_history