# FastAPI server imports
from fastapi import FastAPI
from .routers import posts, users, auth, votes
from . import models
from . database import engine

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# The origins list is a list of domains that can communicate with this backend. If a domain is not listed here, it will be blocked by CORS
# SECURITY BEST PRACTICE IS TO NARROW THIS LIST DOWN AS MUCH AS POSSIBLE AND NOT ALLOW THE PROCESSING OF UNWANTED REQUESTS
origins = []


app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  # allow_methods is also another attribute input arg where we can define what type of HTTP requests will will allow to be sent to our backend
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
def main():
  return {"msg": "main page"}

# Including router for posts endpoints
app.include_router(posts.router)

# Including router for users endpoints
app.include_router(users.router)

# Inlcuding router for auth endpoints
app.include_router(auth.router)

# Including router for vote endpoints
app.include_router(votes.router)



