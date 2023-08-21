from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv, find_dotenv
import time
import os
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

load_dotenv(find_dotenv())
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# while True:
#     try:
#         connection = psycopg2.connect(
#             user=os.environ.get("POSTGRES_USER"),
#             password=os.environ.get("POSTGRES_PASSWORD"),
#             host="localhost",
#             database="fastapi",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = connection.cursor()
#         print("Database connection established.")
#         break
#     except (Exception, psycopg2.Error) as error:
#         print("Error while connecting to PostgreSQL", error)
#         time.sleep(5)


@app.get("/")
def root():
    return {"message": "Welcome to our API"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts;")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    connection.commit()
    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (id,))
    deleted_post = cursor.fetchone()
    connection.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
        (post.title, post.content, post.published, id),
    )
    updated_post = cursor.fetchone()
    connection.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    return {"data": updated_post}
