# FastAPI server imports
from fastapi import APIRouter, status, HTTPException, Depends

# Data Validation imports
from ..DataValidationSchemas import UserCreateRequest, UserCreateResponse, UserLoginRequest

# Database and sqlAlchemy imports
from .. import models
from ..database import engine, get_db
from sqlalchemy.orm import Session

# Hashing imports
from ..utils import hash_password, verify_pwd

router = APIRouter(
  prefix='/auth',
  tags=["Auth"]
)

# POST endpoint to create a user
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def register_user(payload: UserCreateRequest, db: Session = Depends(get_db)):

  user = db.query(models.User).filter(models.User.email == payload.email).first()
  if user:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user with the email you have provided already exists")
  
  payload.password = hash_password(payload.password)
  newUser = models.User(**payload.model_dump())
  db.add(newUser)
  db.commit()
  db.refresh(newUser)
  print(newUser)
  
  return newUser


@ router.post("/login", status_code=status.HTTP_201_CREATED)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):

  
  user = db.query(models.User).filter(models.User.email == payload.email).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect user credentials")
  
  if not verify_pwd(payload.password, user.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect user credentials")

  return { "token": "Example Token" }



  
  
  