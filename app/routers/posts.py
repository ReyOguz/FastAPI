# FastAPI server imports
from fastapi import APIRouter, Response, status, HTTPException, Depends

# Data Validation imports
from ..DataValidationSchemas import PostCreate, PostUpdate, PostResponse

# Database and sqlAlchemy imports
from .. import models
from ..oauth2 import get_current_user
from ..database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)

# GET route to retieve all posts in db
@router.get("/", response_model=list[PostResponse])
def get_all_posts(db: Session = Depends(get_db), currUser = Depends(get_current_user)):
  
  print(currUser.id)
  all_posts = db.query(models.Post).all()
  if not all_posts:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"No Posts in the database")

  return all_posts

# GET route to retireve a post with a specific id
@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db), currUser: int = Depends(get_current_user)):

  post = db.query(models.Post).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} you are looking for was not found")
  
  return post
  
# POST route to create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(payload: PostCreate, db: Session = Depends(get_db), currUser: int = Depends(get_current_user)):
  
  newPost = models.Post(owner_id=currUser.id, **payload.model_dump())
  db.add(newPost)
  db.commit()
  db.refresh(newPost)
  return newPost









# PUT route to update the whole post with a specific id
@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, payload: PostUpdate, db: Session = Depends(get_db), currUser: int = Depends(get_current_user)):
  
  postOfI = db.query(models.Post).filter(models.Post.id == id)

  if not postOfI.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} you are looking to update does not exist")

  if postOfI.first().owner_id != currUser.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorised to perform requested action")
  
  postOfI.update(payload.model_dump(), synchronize_session=False)
  db.commit()

  return postOfI.first()


# DELETE route to delete a post with specific id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), currUser: int = Depends(get_current_user)):
  
  postOfInterest = db.query(models.Post).filter(models.Post.id == id)
  if not postOfInterest.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post you are trying to delete with id: {id} does not exist")
  
  if postOfInterest.first().owner_id != currUser.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorised to perform requested action")

  postOfInterest.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)