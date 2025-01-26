# FastAPI server imports
from fastapi import FastAPI
from .routers import posts, users


app = FastAPI()

# Including router for posts endpoints
app.include_router(posts.router)

# Including router for users endpoints
app.include_router(users.router)



