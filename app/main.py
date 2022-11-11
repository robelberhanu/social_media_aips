from pyexpat import model
import re
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel # used to define schema.
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None

# Connecting to a database
while True:
    try:
        conn = psycopg2.connect(host='localhost', database = 'socialmedia', user='postgres', password='roblion23', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successful")
        break
    except Exception as error:
        print("connection failed")
        print("error:", error)
        time.sleep(2)


# my_posts = [{"title": "title of post 1", "content":"content of post one", "id":1}, {"title": "favorite foods", "content":"I like pizza", "id":2}]

# Helper functions
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id: 
            return i

# root path
@app.get('/')
async def root():
    return{"message":"Hello"}

#get posts path
@app.get('/getposts')
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return{"data":posts}

# send posts to server
@app.post("/createposts", status_code = status.HTTP_201_CREATED)
async def create_posts(post: Post):
     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
     (post.title, post.content, post.published))
     new_post = cursor.fetchone()
     conn.commit()
     return{"data": new_post}

# get single post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                           detail= f'post with id : {id} not found')
    return{"post_detail": post}

# Delete post Endpoint
@app.delete('/deletepost/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Posts
@app.put("/updatepost/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    post_dict = post.dict()
    post_dict['id'] = id

    return {'data': updated_post}



