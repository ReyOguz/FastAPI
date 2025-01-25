from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATABASE_TYPE: str
  DATABASE_USER_NAME: str
  DATABASE_PASSWORD: str
  DATABASE_URL: str
  DATABASE_NAME: str
  DATABASE_PORT_NUMBER: str
  SALT: str

  class Config:
    env_file = ".env"

settings = Settings()