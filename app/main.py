from pyexpat import model
import re
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel # used to define schema.
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    pulished: bool = True
    ratings: Optional[int] = None

try:
    conn = psycopg2.connect(host='localhost', database = 'socialmedia', user='postgres', password='roblion23', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was successful")
except Exception as error:
    print("connection failed")
    print("error:", error)


my_posts = [{"title": "title of post 1", "content":"content of post one", "id":1}, {"title": "favorite foods", "content":"I like pizza", "id":2}]

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
    return{"data":my_posts}

# send posts to server

@app.post("/createposts", status_code = status.HTTP_201_CREATED)
async def create_posts(post: Post):
     post_dict = post.dict()
     post_dict['id'] = randrange(0,1000000)
     my_posts.append(post_dict)
     return{"data": post_dict}

# get single post
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id) 
    if not post:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                           detail= f'post with id : {id} not found')
    return{"post_detail": post}

# Delete post Endpoint
@app.delete('/deletepost/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/updatepost/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {'data': post_dict}



