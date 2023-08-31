from fastapi import FastAPI
from .database import engine
from .routers import users, posts, auth, vote
from . import models
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to our API"}
