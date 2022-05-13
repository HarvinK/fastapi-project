from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .routers import post, user, auth, vote
from .config import settings


# SQLALCHEMY command to auto create tables using the schema defined in models.py
# This command is not required since we've implemted Alembic
# Imports below are required to use this command:
# from . import models
# from .database import engine 
# models.Base.metadata.create_all(bind=engine)

app =FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPI routers 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>FastAPI Project</title>
        </head>
        <body>
            <h1>Welcome to my API</h1>
            <h2><a href="https://www.harvinkaura.xyz/docs">Click Here</a> to test out my application!</h2>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/", response_class=HTMLResponse)
def root():
    return generate_html_response()
    #return {"message": "welcome to my API"}