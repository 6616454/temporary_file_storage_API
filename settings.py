from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str

    redis_host: str
    redis_port: str
    redis_db: str

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600  # Жизнь токена - час


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
