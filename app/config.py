from pydantic import BaseSettings

class Settings(BaseSettings):
    database_password: str 
    database_username: str 
    database_name: str 
    database_port: str
    database_hostname: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = "app/.env"

settings = Settings()