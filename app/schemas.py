from pydantic import BaseModel # used to define schema.
from datetime import datetime


# Base Model For Sending data to Server(Request Schemea For Posts)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
   pass


# Base Model For Sending data to User(Response Schema For Posts)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True
