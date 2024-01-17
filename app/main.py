# Importing necessary modules and functions
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

# Relative imports from the current package
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post, user, auth

# Creating all of the necessary tables in the database
models.Base.metadata.create_all(bind=engine)

# Creating an instance of the FastAPI application
app = FastAPI()

# Including routers from the 'post', 'user', and 'auth' modules
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Defining the root path
@app.get('/')
async def root():
    # When the root path is accessed, return a simple greeting message
    return{"message":"Hello"}