# Here we define the models that represent the tables in our database.

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# ORM MODELS

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Post(Base):
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  
  published = Column(Boolean, server_default="True", nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
  owner = relationship("User")

class Vote(Base):
  
  __tablename__ = "votes"

  post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)



  
