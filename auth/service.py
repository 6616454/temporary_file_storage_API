import datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from jose import jwt, JWTError
from pydantic import ValidationError

from sqlalchemy import select

import tables
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import User, UserCreate
from settings import settings
from .schemas import Token

from exceptions import APIException

import aiofiles.os

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')  # редирект если токен не предоставлен


async def get_current_user(token: str = Depends(oauth_scheme)) -> User:
    return await AuthService.validate_token(token)


class AuthService(APIException):

    @classmethod
    async def validate_token(cls, token: str) -> User:
        """Валидация токена"""
        exception = await cls.create_exception('Could not validate creadentials')

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )  # полезная нагрузка, а именно расшифровка токена
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @staticmethod
    async def verify_password(plain_password: str, hashed_password) -> bool:
        """Валидация пароля, сырой пароль с формы, хэш пароля, которой берется с БД"""
        return bcrypt.verify(plain_password, hashed_password)

    @staticmethod
    async def hash_password(password: str) -> str:
        """Хэширование пароля"""
        return bcrypt.hash(password)

    @staticmethod
    async def create_token(user: tables.User) -> Token:
        user_data = User.from_orm(user)  # из orm в модель Pydantic

        now = datetime.datetime.utcnow()

        payload = {  # формируем у токена payload
            'iat': now,
            'nbf': now,
            'exp': now + datetime.timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )

        return Token(access_token=token)

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_path_for_user(self, username: str):
        try:
            path = f'files/{username}'
            await aiofiles.os.mkdir(path)

        except FileExistsError:

            raise await self.create_exception(
                status_code=422,
                detail='The username is already taken',
                headers=False
            )

        return path

    async def register_new_user(self, user_data: UserCreate) -> Token:

        if user_data.password == user_data.password_correct:
            user = tables.User(
                email=user_data.email,
                username=user_data.username,
                password_hash=await self.hash_password(user_data.password),
                user_path=await self.create_path_for_user(user_data.username)
            )

            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

            return await self.create_token(user)

        raise await self.create_exception(
            "Passwords didn't match",
            status_code=422,
            headers=False
        )

    async def authenticate_user(self, username: str, password: str) -> Token:
        exception = await self.create_exception('Incorrect username or password')

        user = (
            await self.session
            .execute(select(tables.User).filter_by(username=username))
        )

        user = user.scalars().first()

        if not user:
            raise exception

        if not await self.verify_password(password, user.password_hash):
            raise exception

        return await self.create_token(user)
