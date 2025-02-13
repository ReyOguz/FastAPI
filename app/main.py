# THIS IS THE REPO PRE TEST
# FastAPI server imports
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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
  # allow_methods is also another attribute input arg where we can define what type of HTTP requests we will allow to be sent to our backend
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def main():
  return """
  <div style="text-align:center; border: 5px solid transparent; border-image: linear-gradient(to bottom right, #b827fc 0%, #2c90fc 25%, #b8fd33 50%, #fec837 75%, #fd1892 100%); border-image-slice: 1; height: 300px; margin: 20px auto; width: 300px">
    <div>PLEASE NOTE: HTTPS HAS NOT BEEN SET UP AS IT REQUIRES THE PURCHASE OF A DOMAIN.</div>
    <div style="padding-top:30px;"><b>PLEASE DO NOT INPUT ANY SENSITIVE INFORMATION</b></div>
    <div style="padding-top:30px;">Hello and welcome to my first ever deployed backend api! This is a backend only system, there is no frontend. To have a look at the backend functionality available, please navigate to <a href="http://134.199.153.5/docs">this</a> page to see the documentation.</div>
  </div>
  """




# Including router for posts endpoints
app.include_router(posts.router)

# Including router for users endpoints
app.include_router(users.router)

# Inlcuding router for auth endpoints
app.include_router(auth.router)

# Including router for vote endpoints
app.include_router(votes.router)



