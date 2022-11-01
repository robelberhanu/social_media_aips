from pyexpat import model
import re
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel # used to define schema.
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    pulished: bool = True
    ratings: Optional[int] = None

my_posts = [{"title": "title of post 1", "content":"content of post one", "id":1}, {"title": "favorite foods", "content":"I like pizza", "id":2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# root path
@app.get('/')
async def root():
    return{"message":"Hello"}

# get posts path
@app.get('/getposts')
async def get_posts():
    return{"data":my_posts}

# send posts to server

@app.post("/createposts")
async def create_posts(post: Post):
     post_dict = post.dict()
     post_dict['id'] = randrange(0,1000000)
     my_posts.append(post_dict)
     return{"data": post_dict}

# get single post
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)  
    return{"post_detail": post}
