# FastAPI server imports
from fastapi import FastAPI
from .routers import posts, users, auth, votes
from . import models
from . database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Including router for posts endpoints
app.include_router(posts.router)

# Including router for users endpoints
app.include_router(users.router)

# Inlcuding router for auth endpoints
app.include_router(auth.router)

# Including router for vote endpoints
app.include_router(votes.router)



