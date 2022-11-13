from pyexpat import model
import re
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, SessionLocal, get_db

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# Connecting to a database 
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database = 'socialmedia', user='postgres', password='roblion23', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection was successful")
#         break
#     except Exception as error:
#         print("connection failed")
#         print("error:", error)
#         time.sleep(2)


# my_posts = [{"title": "title of post 1", "content":"content of post one", "id":1}, {"title": "favorite foods", "content":"I like pizza", "id":2}]

# Helper functions
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_post_index(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id: 
#             return i

# root path
@app.get('/')
async def root():
    return{"message":"Hello"}

# Get posts path
@app.get("/getposts")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


#get posts path
# @app.get('/getposts')
# async def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return{"data":posts}

# send posts to server
@app.post("/createposts", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #  cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #  (post.title, post.content, post.published))
    #  new_post = cursor.fetchone()
    #  conn.commit()
    new_post =  models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# get single post
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first() # will fine the first post with specified ID only. 
    if not post:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                           detail= f'post with id : {id} not found')
    return post

# Delete post Endpoint
@app.delete('/deletepost/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Posts
@app.put("/updatepost/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()



