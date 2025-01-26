# FastAPI server imports
from fastapi import FastAPI, Response, status, HTTPException, Depends

# Data Validation imports
from .DataValidationSchemas import PostCreate, PostUpdate, PostResponse, UserCreateRequest, UserCreateResponse, UserGetResponse

# Database and sqlAlchemy imports
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

# Hashing imports
from .utils import hash_password


###################################################################################


# For orm db connection
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

################################# POSTS ENDPOINTS #################################

# GET route to retieve all posts in db
@app.get("/posts", response_model=list[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
  all_posts = db.query(models.Post).all()
  if not all_posts:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"No Posts in the database")

  return all_posts

# GET route to retireve a post with a specific id
@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

  post = db.query(models.Post).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} you are looking for was not found")
  
  return post
  
# POST route to create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
  newPost = models.Post(**payload.model_dump())
  db.add(newPost)
  db.commit()
  db.refresh(newPost)
  return newPost


# PUT route to update the whole post with a specific id
@app.put("/posts/{id}", response_model=PostResponse)
def update_post(id: int, payload: PostUpdate, db: Session = Depends(get_db)):
  
  postOfI = db.query(models.Post).filter(models.Post.id == id)
  if not postOfI.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} you are looking to update does not exist")

  postOfI.update(payload.model_dump(), synchronize_session=False)
  db.commit()

  return postOfI.first()


# DELETE route to delete a post with specific id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  
  postOfInterest = db.query(models.Post).filter(models.Post.id == id)
  if not postOfInterest.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post you are trying to delete with id: {id} does not exist")
  
  postOfInterest.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)
  
################################# POSTS ENDPOINTS #################################

################################# USERS ENDPOINTS #################################


# POST endpoint to create a user
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
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


@app.get("/users/{id}", status_code=status.HTTP_200_OK,  response_model=UserGetResponse)
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user you are looking for could not be found")

  return user
  