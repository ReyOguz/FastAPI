# FastAPI server imports
from fastapi import FastAPI, Response, status, HTTPException, Depends

# Data Validation imports
from .DataValidationSchemas import Post

# Database and sqlAlchemy imports
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

###################################################################################

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Get route for simple home url hit.
@app.get("/")
def root():
  return {"response": "Welcome to the home page"}

# GET route to retieve all posts in db
@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
  all_posts = db.query(models.Post).all()
  if not all_posts:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"No Posts in the database")

  return { "posts": all_posts}
  
# POST route to create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post, db: Session = Depends(get_db)):
  newPost = models.Post(**payload.model_dump())
  db.add(newPost)
  db.commit()
  db.refresh(newPost)
  return {"data": payload}
  


# GET route to retireve a post with a specific id
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):

  post = db.query(models.Post).filter(models.Post.id == id).first()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"The post with id {id} you are looking for was not found")
  
  return { "response": post}
 


# DELETE route to delete a post with specific id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  
  postOfInterest = db.query(models.Post).filter(models.Post.id == id)
  if not postOfInterest.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post you are trying to delete with id: {id} does not exist")
  
  postOfInterest.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)
  

# PUT route to update the whole post with a specific id
@app.put("/posts/{id}")
def update_post(id: int, payload: Post, db: Session = Depends(get_db)):
  
  postOfI = db.query(models.Post).filter(models.Post.id == id)

  if not postOfI.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} you are looking to update does not exist")

  
  postOfI.update(payload.model_dump(), synchronize_session=False)
  db.commit()

  return {"response": "Post successfully updated"}

  

  
  



  
  
  