from pyexpat import model
import re
from typing import Optional, List
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




# root path
@app.get('/')
async def root():
    return{"message":"Hello"}


####################################################### POSTS ########################################################

# Get posts path
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



# send posts to server
@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post =  models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# get single post
@app.get("/posts/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
  
    post = db.query(models.Post).filter(models.Post.id == id).first() # will fine the first post with specified ID only. 
    if not post:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                           detail= f'post with id : {id} not found')
    return post

# Delete post Endpoint
@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
   
    post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Posts
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


#########################################################End Posts #########################################################


######################################################## Account Services ######################################################

# path operation to create users.
@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user =  models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user =  models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
