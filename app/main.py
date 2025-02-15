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
origins = ["*"]

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
  <!DOCTYPE html>
  <html>
      <head>
          <meta charset="UTF-8">
          <title>Rey's FastAPI Backend Project</title>
        <style>
          body {
            font-family: 'Arial Light', sans-serif;
            padding: 0 10%;
          }

          h1 {
            font-size: 6vh;
            font-weight: lighter;
            text-align: center;
            margin: 0;
            margin-top: 0.67em;
            color: #076025;
            font-size: 3em;
          }

          h2 {
            color: #208b44;
            font-size: 4vh;
            font-weight: normal;
            text-align: center;
            font-size: 2em;
          }

          hr {
            background-color: #CCC;
            border: none;
            height: 1px;
          }
          p {
            color: #666666;
            font-size: 1.4em;
            font-weight: lighter;
            letter-spacing: 0;
            line-height: 2;
            margin: 0;
          }

          .centred {
            text-align: center;
          }
          .warning {
            font-size: 1.7em;
            color: red;
          }

          .half-card {
            flex: 1;
            padding: 0 2%;
          }
        </style>
      </head>

      <body>
          <h1 style="padding-top: 40px; padding-bottom: 30px;">Hello and welcome! My Name Is Oguzhan (Rey), Im A Recent Computer Science Graduate.</h1>

          <div class="columned">
            <div class="half-card">
              <h2>This Is The Landing Page For My First Ever Deployed Project! - A FastAPI Backend.</h2>
              <p class="centred">
                This landing page is made with simple HTML. I only added it to greet visitors and it is by no means a focus on the frontend.
                If you would like to checkout the backend functionality for the FastAPI project, click <a href="http://134.199.153.5/docs">here</a> to be take to the API documentation page.
                You can interact with the system by first registering and then logging in with the same credentials. Although HTTPS has been enabled with SSL/TLS and a firewall has been set up, please keep in mind that this is a hobby project.
              </p>
              <p class="centred warning" style="padding-top: 30px;">
                <b>PLEASE DO NOT ENTER ANY SENSITIVE INFORMATION</b>
              </p>
              
            </div>
          </div>
          <br /><br /><hr /><br /><br />
          <h2>Links To Other Projects</h2>
          <p class="centred">
            If you would like to see some of my other projects, click <a href="https://github.com/ReyOguz?tab=repositories&q=&type=public&language=&sort=">here</a> to visit my GitHub profile, where you can find the public repository for this and other projects. However, keep in mind that this is the only deployed one.
          </p>
          <br /><br /><hr /><br /><br />
          <div class="columned">
            <div class="half-card">
              <h2>Contact Information</h2>
              <p class="centred" style="padding-bottom: 30px">
                If you're reading this, you most likely have my email and LinkedIn profile. But to make things simpler, click <a href="https://www.linkedin.com/in/oguzhan-rey-oguz/">here</a> to visit my LinkedIn profile.
              </p>
            </div>
          </div>
          <br /><br /><hr /><br /><br />
          <h1 style="text-align:center; border: 10px solid transparent; border-image: linear-gradient(to bottom right, #076025 0%, #24bf58 50%, #076025 100%); border-image-slice: 1; height: auto; margin: 20px auto; width: 420px">Have A Nice Day!</h1>
      </body>
  </html>
  """




# Including router for posts endpoints
app.include_router(posts.router)

# Including router for users endpoints
app.include_router(users.router)

# Inlcuding router for auth endpoints
app.include_router(auth.router)

# Including router for vote endpoints
app.include_router(votes.router)



