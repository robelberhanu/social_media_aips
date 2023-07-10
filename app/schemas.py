from pydantic import BaseModel, EmailStr # used to define schema.
from datetime import datetime
from typing import Optional


# Base Model For Sending data to Server(Request Schemea For Posts)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
   pass


# Base Model For Sending data to User(Response Schema For Posts)

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData():
    id: Optional[str]