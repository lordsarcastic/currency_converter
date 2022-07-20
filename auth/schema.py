from datetime import datetime
from typing import Optional
from uuid import UUID

from db.schema import BaseSchema


class LoginSchema(BaseSchema):
    email: str
    password: str


class SignupSchema(BaseSchema):
    email: str
    first_name: str
    last_name: Optional[str]
    password: str


class UserSchema(BaseSchema):
    email: str
    first_name: str
    last_name: Optional[str]
    created_at: datetime


class TokenSchema(BaseSchema):
    access_token: str
    refresh_token: str


class AuthSchema(BaseSchema):
    expiry: datetime
    data: UserSchema