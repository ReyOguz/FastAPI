import jwt
from jwt.exceptions import InvalidTokenError
from .config import settings
from datetime import datetime, timedelta

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
  # We dont want to alter the input data so we make a copy
  to_encode = data.copy()

  # expiration time is just current time add minutes we want the token to be valid
  expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  
  # update the payload to encode part
  to_encode.update({ "exp": expire})

  # create token by encoding updated payload, secret key using specified algorithm
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  # return created token
  return encoded_jwt