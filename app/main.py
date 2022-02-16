from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='thisisnotatest1!',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(2)

my_posts = [{
    "title": "Bitcoin to the moon",
    "content": "Bear market ):, it will eventually!",
    "id": 1
}, {
    "title": "Elon Musk is amazing",
    "content": "Started from the bottom now he's here",
    "id": 2
}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")
def root():
    return {"message": "Welcome to my API!!!"}


@app.get("/posts")
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return {"data": posts}


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning *""", (
        post.title,
        post.content,
        post.published
    ))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# routes top down


@app.get("/posts/latest")
def get_latest_posts():
    post = my_posts[len(my_posts)-1]
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""select * from posts where id=%s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found!")
    return {"data": post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(
        """delete from posts where id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""", (
        post.title,
        post.content,
        post.published,
        str(id)
    ))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist!")
    return {"data": updated_post}
