from datetime import datetime
from typing import Optional

from db.schema import BaseSchema


class LoginSchema(BaseSchema):
    """
    Does not exactly handle login, instead it is used as the parser
    for the login service
    """
    email: str
    password: str


class SignupSchema(BaseSchema):
    """
    Handles request body parsing for signup
    """
    email: str
    first_name: str
    last_name: Optional[str]
    password: str


class UserSchema(BaseSchema):
    """
    Details of a user in the API
    """
    email: str
    first_name: str
    last_name: Optional[str]
    created_at: datetime


class TokenSchema(BaseSchema):
    """
    Handles token for authentication and authorization
    """
    access_token: str
    refresh_token: str


class AuthSchema(BaseSchema):
    """
    Handles encoded information for user and expiry date for tokens
    """
    expiry: datetime
    data: UserSchema
