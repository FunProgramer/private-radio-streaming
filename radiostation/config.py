from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_server: str

    max_str_length: int = 255


settings = Settings()
