from datetime import datetime, timedelta
import logging
from typing import Any, Dict, Optional

from jose import jwt
from pydantic import ValidationError

from backend.services import BaseService
from backend.settings import settings

from .models import User
from .schema import AuthSchema, LoginSchema, SignupSchema, TokenSchema, UserSchema
from . import exceptions



def hash_password(password: str) -> str:
    hashed_password = settings.PASSWORD_HASHER.hash(password)
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_is_verified = settings.PASSWORD_HASHER.verify(
        plain_password,
        hashed_password
    )

    return bool(password_is_verified)

def create_auth_token(payload: Dict[str, Any], expiry: int) -> str:
    expiry_delta = datetime.utcnow() + timedelta(seconds=expiry)
    data_to_encode = {
        "expiry": str(expiry_delta),
        "data": payload
    }
    encoded_data: str = jwt.encode(
        data_to_encode,
        settings.SECRET_KEY,
        settings.JWT_ALGORITHM
    )

    return encoded_data


class UserService(BaseService):
    def create_user(self, user: SignupSchema) -> User:
        user_from_db = self.db.query(User).filter(
            User.email == user.email
        ).first()

        if user_from_db:
            raise exceptions.UserExist
        
        user.password = hash_password(user.password)
        user_to_save = User(**user.to_dict())
        self.db.add(user_to_save)
        self.db.commit()
        self.db.refresh(user_to_save)
        result = UserSchema(**User.to_dict(user_to_save))
        return result

    
    def login(self, credentials: LoginSchema) -> TokenSchema:
        user_from_db: Optional[User] = self.db.query(User).filter(
            User.email == credentials.email
        ).first()

        if not user_from_db:
            raise exceptions.InvalidCredentials
        
        if not verify_password(credentials.password, user_from_db.password):
            raise exceptions.InvalidCredentials

        user = User.to_dict(user_from_db)
        user.pop('password')
        token = TokenSchema(
            access_token=create_auth_token(user, settings.ACCESS_TOKEN_EXPIRY_TIME),
            refresh_token=create_auth_token(user, settings.REFRESH_TOKEN_EXPIRY_TIME)
        )
        return token

    def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            logging.info(payload)
            token_data = AuthSchema(**payload)
            
            if token_data.expiry > datetime.now():
                raise exceptions.TokenExpired
        except(jwt.JWTError, ValidationError):
            raise exceptions.UnvalidatedCredentials
            
        user_from_db: Optional[User] = self.db.query(User).filter(
            User.email == token_data.data.email
        ).first()
        
        
        if user_from_db is None:
            raise exceptions.UserDoesNotExist
        
        return user_from_db
