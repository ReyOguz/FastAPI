import jwt
from jwt.exceptions import InvalidTokenError
from .config import settings
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from .DataValidationSchemas import TokenData
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
  # We dont want to alter the input data so we make a copy
  to_encode = data.copy()

  # expiration time is just current time add minutes we want the token to be valid
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  
  # update the payload to encode part
  to_encode.update({ "exp": expire})

  # create token by encoding updated payload, secret key using specified algorithm
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  # return created token
  return encoded_jwt

def verify_access_token(token: str):
  credentials_exception = HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"} ) 
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    userId = payload.get("user_id", None)

    if not userId:
      raise credentials_exception

    token_data = TokenData(id=userId)
  except InvalidTokenError:
    raise credentials_exception
  
  return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
  return verify_access_token(token)
