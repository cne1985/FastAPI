from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()