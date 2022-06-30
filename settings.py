from pydantic import BaseSettings


class Settings(BaseSettings):
    pass


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
