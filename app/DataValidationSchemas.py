from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class PostBase(BaseModel):
  id: int
  title: str
  content: str
  published: bool = True

class PostCreate(PostBase):
  pass

class PostUpdate(PostBase):
  pass

class PostResponseVote(BaseModel):
  Post: PostBase
  votes: int

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

class VoteRequest(BaseModel):
  post_id: int
  direction: Literal[-1,1]