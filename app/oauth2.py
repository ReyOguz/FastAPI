import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from .config import settings
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from .DataValidationSchemas import TokenData
from fastapi.security import OAuth2PasswordBearer

from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models

# Piece of code that extracts the JWT token from the header of a request
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
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"}
  ) 
  try:
    # decode extracted jwt token into payload dict
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    
    # retrieve user id from decoded payload
    userId = payload.get("user_id")

    # if the credentials are invalid, raise an exception
    if not userId:
      raise credentials_exception

    token_data = TokenData(id=userId)
  except ExpiredSignatureError:
    credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Token has expired, please login again.", 
      headers={"WWW-Authenticate": "Bearer"} 
    ) 
    raise credentials_exception
  except InvalidTokenError:
    raise credentials_exception
  
  return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

  token = verify_access_token(token)
  currUser = db.query(models.User).filter(models.User.id == token.id).first()
  
  return currUser
