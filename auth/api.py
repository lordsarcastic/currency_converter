from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.exceptions import UserDoesNotExist

from db.db import get_db

from .models import User
from .schema import LoginSchema, SignupSchema, TokenSchema, UserSchema
from .services import UserService, reuseable_oauth


router = APIRouter(
    prefix="/user"
)


def get_user(db: Session = Depends(get_db), token: str = Depends(reuseable_oauth)) -> User:
    user = UserService(db).get_current_user(token)
    
    return user

@router.post('/signup', summary="Create a new user", response_model=UserSchema)
def signup(user: SignupSchema, db: Session = Depends(get_db)):
    created_user = UserService(db).create_user(user)
    return created_user

@router.post('/login', summary="Log in a user", response_model=TokenSchema)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    credentials = LoginSchema(
        email=form.username,
        password=form.password
    )
    token = UserService(db).login(credentials)
    return token

@router.get('/me', summary="Get details of logged in user", response_model=UserSchema)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(reuseable_oauth)):
    user = UserService(db).get_current_user(token)
    schema = UserSchema(**User.to_dict(user))
    return schema