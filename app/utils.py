# Hashing imports
from passlib.context import CryptContext
from .config import settings

# Context for hashing passwords
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
  password += settings.SALT
  return pwd_content.hash(password)

def verify_pwd(plain, stored):
  plain += settings.SALT
  return pwd_content.verify(plain, stored)