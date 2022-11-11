# This class represents our database tables.

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tabelname__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable = True, default = True)

