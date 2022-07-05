from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    username: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    """Пользователь, которого мы будем доставать через БД"""
    id: int
    user_path: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
