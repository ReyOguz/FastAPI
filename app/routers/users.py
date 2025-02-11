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

router = APIRouter(
  prefix="/users",
  tags=['Users']
)



@router.get("/{id}", status_code=status.HTTP_200_OK,  response_model=UserGetResponse)
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user you are looking for could not be found")

  return user

