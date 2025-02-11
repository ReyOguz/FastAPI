from fastapi import APIRouter, Response, status, HTTPException, Depends

# Schema imports
from ..DataValidationSchemas import VoteRequest

# Database and sqlAlchemy imports
from .. import models
from ..oauth2 import get_current_user
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix='/vote',
  tags=["Votes"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def vote(payload: VoteRequest, db: Session = Depends(get_db), currUser = Depends(get_current_user)):
  
  user_id = currUser.id
  post_id = payload.post_id
  vote_dir = payload.direction

  post_query = db.query(models.Post).filter(models.Post.id == post_id).first()
  if not post_query:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post does not exist")

  vote_query = db.query(models.Vote).filter(models.Vote.post_id == post_id, models.Vote.user_id == user_id)

  if vote_dir == 1: # add vote
    if vote_query.first():
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user_id} has already votes for post {post_id}")
    else:
      newVote = models.Vote(post_id=payload.post_id, user_id=currUser.id)
      db.add(newVote)
      db.commit()
      return { "msg": "successfully voted" }
  else: # remove vote
    if not vote_query.first():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
    else:
      vote_query.delete(synchronize_session=False)
      newVote = models.Vote(post_id=payload.post_id, user_id=currUser.id)
      db.commit()
      
      return Response(status_code=status.HTTP_204_NO_CONTENT)


  