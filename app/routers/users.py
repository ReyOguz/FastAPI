# FastAPI server imports
from fastapi import APIRouter, status, HTTPException, Depends

# Data Validation imports
from ..DataValidationSchemas import UserCreateRequest, UserCreateResponse, UserGetResponse

# Database and sqlAlchemy imports
from .. import models
from ..database import engine, get_db
from sqlalchemy.orm import Session

# Hashing imports
from ..utils import hash_password

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
  prefix="/users",
  tags=['Users']
  
)

# POST endpoint to create a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def create_user(payload: UserCreateRequest, db: Session = Depends(get_db)):

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


@router.get("/{id}", status_code=status.HTTP_200_OK,  response_model=UserGetResponse)
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user you are looking for could not be found")

  return user

