from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv, find_dotenv
import time
import os

app = FastAPI()

load_dotenv(find_dotenv())


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        connection = psycopg2.connect(
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host="localhost",
            database="fastapi",
            cursor_factory=RealDictCursor,
        )
        cursor = connection.cursor()
        print("Database connection established.")
        break
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        time.sleep(5)

@app.get("/")
def root():
    return {"message": "Welcome to the API"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = next((post for post in my_posts if post["id"] == id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100)
    my_posts.append(post_dict)
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = next((post for post in my_posts if post["id"] == id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post = next((post for post in my_posts if post["id"] == id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    post.update(post.dict())
    return {"data": post}
