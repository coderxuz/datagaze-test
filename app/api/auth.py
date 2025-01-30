from typing import Annotated
from securely import Auth
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas import UserSign, TokenRes, UserLogin
from app.database import get_async_db
from app.models import User

from datetime import timedelta
from os import getenv



load_dotenv()
SECRET_KEY = getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY didn't find")

auth = Auth(access_token_expires=timedelta(1), refresh_token_expires=timedelta(7), secret_key=SECRET_KEY)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/swagger")

router = APIRouter(prefix='/auth', tags=['AUTH'])

@router.post('/sign', response_model=TokenRes)
async def sign_up(data:UserSign, db:AsyncSession=Depends(get_async_db)):
    username_exist = (await db.execute(select(User).where(User.username == data.username))).first()
    if username_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='username exist in db'
        )
        
    new_user = User(
        name=data.name,
        surname=data.surname,
        username=data.username,
        password=auth.hash_password(data.password)
    )
    db.add(new_user)
    await db.commit()
    return auth.create_tokens(subject=data.username)

@router.post(
    '/login', response_model=TokenRes
)
async def login(data:UserLogin,db:AsyncSession= Depends(get_async_db)):
    db_user = (await db.execute(select(User).where(User.username == data.username))).scalars().first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials'
        )
    if not auth.verify_password(plain_password=data.password, hashed_password=db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials'
        )
    return auth.create_tokens(subject=data.username)

@router.post(
    '/swagger'
)
async def swagger(data:Annotated[OAuth2PasswordRequestForm, Depends()],db:AsyncSession= Depends(get_async_db)):
    db_user = (await db.execute(select(User).where(User.username == data.username))).scalars().first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials'
        )
    if not auth.verify_password(plain_password=data.password, hashed_password=db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials'
        )
    tokens = auth.create_tokens(subject=data.username)
    return {"access_token": tokens['accessToken'], "token_type": "bearer"}