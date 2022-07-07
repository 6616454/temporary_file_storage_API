from pydantic import BaseModel, EmailStr, Field, validator


class BaseUser(BaseModel):
    email: EmailStr
    username: str


class UserCreate(BaseUser):
    password: str = Field(..., min_length=6)
    password_correct: str


class User(BaseUser):
    """Пользователь, которого мы будем доставать через БД"""
    id: int
    user_path: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
