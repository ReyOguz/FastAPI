from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True

class PostCreate(PostBase):
  pass

class PostUpdate(PostBase):
  pass

class PostResponse(PostBase):
  id: int

  class Config:
    from_attributes = True


class UserCreateRequest(BaseModel):
  email: EmailStr
  password: str

class UserCreateResponse(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

  class Config:
    from_attributes = True
