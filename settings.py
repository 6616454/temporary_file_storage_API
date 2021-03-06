from pydantic import BaseSettings


class Settings(BaseSettings):
    time_to_delete: int  # YOUR VALUE

    database_url: str

    redis_host: str
    redis_port: str
    redis_db: str

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600  # Жизнь токена - час

    main_link: str
    token_api: str


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
