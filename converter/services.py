import json
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

import requests
from auth.models import User

from backend.services import BaseService
from backend.settings import settings
from db.db import RedisClient

from . import exceptions
from .models import ConversionHistory
from .schema import (
    ConversionResponseSchema,
    ConvertSchema,
    CurrencyListSchema,
    CurrencySchema,
    GetHistorySchema,
    HistorySchema,
)


CONVERSION_APIS = [
    "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{}/{}.min.json",
    "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{}/{}.json",
    "https://raw.githubusercontent.com/fawazahmed0/currency-api/1/latest/currencies/{}/{}.min.json",
    "https://raw.githubusercontent.com/fawazahmed0/currency-api/1/latest/currencies/{}/{}.json",
]


def make_request(url, **kwargs) -> Dict[str, Any]:
    """
    Non-generic utility to make a request to the given URL.
    """
    response = requests.get(url, **kwargs)
    response.raise_for_status()
    return response.json()


def make_request_with_retries(urls, **kwargs) -> Dict[str, Any]:
    response = None

    for url in urls:
        try:
            response = make_request(url, **kwargs)
            break
        except requests.HTTPError:
            continue

    return response


def craft_conversion_urls(_from, to):
    urls = list(map(lambda url: url.format(_from, to), CONVERSION_APIS))

    return urls


class ConverterService(BaseService):
    CURRENCIES_REDIS_KEY = "currencies"

    def add_history(self, history: HistorySchema) -> None:
        history_to_save = ConversionHistory(**history.to_dict())
        self.save(history_to_save)

    @classmethod
    def cache_currency_list(cls):
        if RedisClient.get(cls.CURRENCIES_REDIS_KEY):
            return

        url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.min.json"

        try:
            currencies = make_request(url)
        except requests.HTTPError:
            raise exceptions.APIIsDown

        jsonified_currencies = json.dumps(currencies)
        logging.info(jsonified_currencies)
        RedisClient.setex(
            cls.CURRENCIES_REDIS_KEY,
            settings.CURRENCY_CACHE_EXPIRY_TIME,
            jsonified_currencies,
        )

    @classmethod
    def get_currency_list(cls) -> Dict[str, str]:
        currencies: str = RedisClient.get(cls.CURRENCIES_REDIS_KEY)
        print("We grab from cache")
        if not currencies:
            print("We are grabbing from cached")
            cls.cache_currency_list()
            currencies = RedisClient.get(cls.CURRENCIES_REDIS_KEY)

        return json.loads(currencies)

        # list_of_currencies = list()

        # for key, value in json.loads(currencies):
        #     list_of_currencies.append(
        #         CurrencySchema(code=key, name=value)
        #     )

        # return CurrencyListSchema(currencies=list_of_currencies)

    @classmethod
    def currency_is_supported(cls, currency: str) -> bool:
        currency_from_cache = cls.get_currency_list().get(currency)
        return bool(currency_from_cache)

    @classmethod
    def convert(cls, payload: ConvertSchema) -> ConversionResponseSchema:
        conversion_urls = craft_conversion_urls(
            payload.from_currency, payload.to_currency
        )
        rate = make_request_with_retries(conversion_urls).get(payload.to_currency)

        result = ConversionResponseSchema(
            rate=rate, result=rate * payload.amount, **payload.to_dict()
        )

        return result

    def store_conversion_to_history(
        self, payload: ConversionResponseSchema, user: UUID
    ):
        history_to_db = ConversionHistory(**payload.to_dict(), user_id=user)
        self.save(history_to_db)

    def get_conversion_history(
        self, payload: GetHistorySchema, user: User
    ) -> List[ConversionHistory]:
        histories = self.db.query(ConversionHistory).filter(
            ConversionHistory.user == user
        )
        if currency := payload.from_currency:
            histories = histories.filter(ConversionHistory.from_currency == currency)
        if currency := payload.to_currency:
            histories = histories.filter(ConversionHistory.to_currency == currency)

        histories: List[ConversionHistory] = histories.all()

        return histories
