from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATABASE_TYPE: str
  DATABASE_USER_NAME: str
  DATABASE_PASSWORD: str
  DATABASE_URL: str
  DATABASE_NAME: str
  DATABASE_PORT_NUMBER: str
  SALT: str
  JWT_SECRET_KEY: str
  JWT_ALGORITHM: str

  class Config:
    env_file = ".env"

settings = Settings()