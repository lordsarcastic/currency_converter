import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from backend.services import BaseService
from backend.settings import settings

from . import exceptions
from .models import User
from .schema import AuthSchema, LoginSchema, SignupSchema, TokenSchema, UserSchema

# for authentication that works seamlessly with OpenAPI
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/user/login",
    scheme_name="JWT"
)


def hash_password(password: str) -> str:
    """Creates a hash of the password"""
    hashed_password = settings.PASSWORD_HASHER.hash(password)
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a password corresponds to a hash"""
    password_is_verified = settings.PASSWORD_HASHER.verify(
        plain_password, hashed_password
    )

    return bool(password_is_verified)


def create_auth_token(payload: Dict[str, Any], expiry: int) -> str:
    """
    This handles the encoding of user information into a token
    that can be used. It is generic so as to accomodate access and
    refresh token.
    """
    expiry_delta = datetime.now() + timedelta(seconds=expiry)
    data_to_encode = {"expiry": str(expiry_delta), "data": payload}
    encoded_data: str = jwt.encode(
        data_to_encode, settings.SECRET_KEY, settings.JWT_ALGORITHM
    )

    return encoded_data


class UserService(BaseService):
    """
    Core functionality for user-related tasks.
    """
    def create_user(self, user: SignupSchema) -> User:
        """
        Creates a user from signup details
        """
        user_from_db = self.db.query(User).filter(
            User.email == user.email
        ).first()

        if user_from_db:
            raise exceptions.UserExist

        user.password = hash_password(user.password)
        user_to_save = User(**user.to_dict())
        self.save(user_to_save)
        result = UserSchema(**User.to_dict(user_to_save))
        return result

    def login(self, credentials: LoginSchema) -> TokenSchema:
        """
        Confirms a user and grants an access and refresh token if
        credentials are valid.
        """
        user_from_db: Optional[User] = self.db.query(User).filter(
            User.email == credentials.email
        ).first()

        if not user_from_db:
            raise exceptions.InvalidCredentials

        if not verify_password(credentials.password, user_from_db.password):
            raise exceptions.InvalidCredentials

        user = User.to_dict(user_from_db)
        # we don'w want the password hash to be visible in
        # the token information
        user.pop("password")
        token = TokenSchema(
            access_token=create_auth_token(
                user,
                settings.ACCESS_TOKEN_EXPIRY_TIME
            ),
            refresh_token=create_auth_token(
                user,
                settings.REFRESH_TOKEN_EXPIRY_TIME
            ),
        )
        return token

    def get_current_user(self, token: str) -> User:
        """
        Returns a user from a token
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            logging.info(payload)
            token_data = AuthSchema(
                expiry=datetime.fromisoformat(payload['expiry']),
                data=payload['data']
            )

            # if the expiry date is in the pas
            if token_data.expiry < datetime.now():
                raise exceptions.TokenExpired
        except (jwt.JWTError, ValidationError):
            raise exceptions.UnvalidatedCredentials

        user_from_db: Optional[User] = self.db.query(User).filter(
            User.email == token_data.data.email
        ).first()

        if user_from_db is None:
            raise exceptions.UnvalidatedCredentials

        return user_from_db
