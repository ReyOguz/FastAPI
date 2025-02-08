from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True

class PostCreate(PostBase):
  pass

class PostUpdate(PostBase):
  pass



class UserCreateRequest(BaseModel):
  email: EmailStr
  password: str

class UserCreateResponse(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

  class Config:
    from_attributes = True

class PostResponse(PostBase):
  id: int
  owner_id: int
  owner: UserCreateResponse

  class Config:
    from_attributes = True

class UserGetResponse(UserCreateResponse):
  pass


class UserLoginRequest(UserCreateRequest):
  pass

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[int]