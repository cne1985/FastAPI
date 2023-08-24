from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import users, posts, auth


load_dotenv(find_dotenv())
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to our API"}
